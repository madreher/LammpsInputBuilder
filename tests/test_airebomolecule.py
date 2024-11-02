from pathlib import Path
import tempfile
from uuid import uuid4
import os
import shutil

import pytest

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, \
    Forcefield, MoleculeFileFormat
from lammpsinputbuilder.typedmolecule import AireboTypedMolecularSystem
from lammpsinputbuilder.types import LammpsUnitSystem


def test_empty_airebo_molecule():
    # Create an empty molecule 
    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    assert typed_molecule.get_forcefield_type() is None
    assert typed_molecule.get_boundingbox_style() == BoundingBoxStyle.PERIODIC
    assert typed_molecule.get_electrostatic_method() == ElectrostaticMethod.QEQ
    assert typed_molecule.get_unit_system() == LammpsUnitSystem.METAL
    assert typed_molecule.get_default_thermo_variables() == ['step', 'v_REBO', 'v_LJ', 'v_TORSION']
    assert typed_molecule.get_lammps_data_filename() == "model.data"

    assert not typed_molecule.is_model_loaded()

    assert typed_molecule.get_molecule_content() == ""
    assert typed_molecule.get_molecule_format() is None
    assert typed_molecule.get_molecule_name() is None

    assert typed_molecule.get_forcefield_content() == ""
    assert typed_molecule.get_forcefield_name() is None



def test_airebo_molecule_from_file():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    assert typed_molecule.get_forcefield_type() == Forcefield.AIREBO
    assert typed_molecule.get_boundingbox_style() == BoundingBoxStyle.PERIODIC
    assert typed_molecule.get_electrostatic_method() == ElectrostaticMethod.QEQ
    
    assert typed_molecule.is_model_loaded()

    assert typed_molecule.get_molecule_content() != ""
    assert typed_molecule.get_molecule_format() == MoleculeFileFormat.XYZ
    assert typed_molecule.get_molecule_name()  == Path(molecule_path.name)

    assert typed_molecule.get_forcefield_content() != ""
    assert typed_molecule.get_forcefield_name() == Path(forcefield_path.name)


def test_airebo_molecule_from_strings():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    molecule_content = ""
    potential_content = ""
    with open(molecule_path, 'r', encoding="utf-8") as f:
        molecule_content = f.read()
    with open(forcefield_path, 'r', encoding="utf-8") as f:
        potential_content = f.read()

    typed_molecule.load_from_string(molecule_content, MoleculeFileFormat.XYZ, potential_content, Path(forcefield_path.name), Path(molecule_path.name))

    assert typed_molecule.get_forcefield_type() == Forcefield.AIREBO
    assert typed_molecule.get_boundingbox_style() == BoundingBoxStyle.PERIODIC
    assert typed_molecule.get_electrostatic_method() == ElectrostaticMethod.QEQ
    
    assert typed_molecule.is_model_loaded()

    assert typed_molecule.get_molecule_content() == molecule_content
    assert typed_molecule.get_molecule_format() == MoleculeFileFormat.XYZ
    assert typed_molecule.get_molecule_name()  == Path(molecule_path.name)

    assert typed_molecule.get_forcefield_content() == potential_content
    assert typed_molecule.get_forcefield_name() == Path(forcefield_path.name)


def test_molecule_to_dict():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    result = typed_molecule.to_dict()

    assert result["class_name"] == "AireboTypedMolecularSystem"
    assert result["electrostatic_method"] == ElectrostaticMethod.QEQ.value
    assert result["forcefield_name"] == str(forcefield_path.name)
    assert result["molecule_name"] == str(molecule_path.name)
    assert result["molecule_format"] == MoleculeFileFormat.XYZ.value
    assert result["forcefield_content"] == typed_molecule.get_forcefield_content()
    assert result["molecule_content"] == typed_molecule.get_molecule_content()

def test_molecule_to_dict_to_molecule():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    dict1 = typed_molecule.to_dict()

    typed_molecule2 = AireboTypedMolecularSystem()
    typed_molecule2.from_dict(dict1, 0)

    assert typed_molecule.to_dict() == typed_molecule2.to_dict()

def test_moleculeToJobFolder():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    job_folder = Path(tempfile.gettempdir()) / str(uuid4())
    os.makedirs(job_folder)

    moleculeHolder = typed_molecule.generate_lammps_data_file(job_folder)
    input_path = typed_molecule.generate_lammps_input_file(job_folder, moleculeHolder)

    assert moleculeHolder is not None
    assert input_path == job_folder / "lammps.input"
    assert (job_folder / "molecule.XYZ").is_file()
    assert (job_folder / typed_molecule.get_lammps_data_filename()).is_file()
    assert (job_folder / "model.data").is_file()
    assert (job_folder / "model.data.temp").is_file()

    shutil.rmtree(job_folder, ignore_errors=True)