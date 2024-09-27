import pytest

from pathlib import Path
import tempfile
from uuid import uuid4
import os
import shutil

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, Forcefield, MoleculeFileFormat
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecularSystem


def test_emptyReaxMolecule():
    # Create an empty molecule 
    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    assert typedMolecule.getForcefieldType() == Forcefield.REAX
    assert typedMolecule.getBoundingBoxStyle() == BoundingBoxStyle.PERIODIC
    assert typedMolecule.getElectrostaticMethod() == ElectrostaticMethod.QEQ
    
    assert not typedMolecule.isModelLoaded()

    assert typedMolecule.getMoleculeContent() == ""
    assert typedMolecule.getMoleculeFormat() is None 
    assert typedMolecule.getMoleculePath() is None

    assert typedMolecule.getForcefieldContent() == ""
    assert typedMolecule.getForcefieldPath() is None



def test_reaxMoleculeFromFile():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(molecule_path, forcefieldPath)

    assert typedMolecule.getForcefieldType() == Forcefield.REAX
    assert typedMolecule.getBoundingBoxStyle() == BoundingBoxStyle.PERIODIC
    assert typedMolecule.getElectrostaticMethod() == ElectrostaticMethod.QEQ
    
    assert typedMolecule.isModelLoaded()

    assert typedMolecule.getMoleculeContent() != ""
    assert typedMolecule.getMoleculeFormat() == MoleculeFileFormat.XYZ
    assert typedMolecule.getMoleculePath()  == molecule_path

    assert typedMolecule.getForcefieldContent() != ""
    assert typedMolecule.getForcefieldPath() == forcefieldPath


def test_reaxMoleculeFromStrings():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    molecule_content = ""
    potentialContent = ""
    with open(molecule_path, 'r') as f:
        molecule_content = f.read()
    with open(forcefieldPath, 'r') as f:
        potentialContent = f.read()

    typedMolecule.loadFromStrings(molecule_content, MoleculeFileFormat.XYZ, potentialContent, forcefieldPath, molecule_path)

    assert typedMolecule.getForcefieldType() == Forcefield.REAX
    assert typedMolecule.getBoundingBoxStyle() == BoundingBoxStyle.PERIODIC
    assert typedMolecule.getElectrostaticMethod() == ElectrostaticMethod.QEQ
    
    assert typedMolecule.isModelLoaded()

    assert typedMolecule.getMoleculeContent() == molecule_content
    assert typedMolecule.getMoleculeFormat() == MoleculeFileFormat.XYZ
    assert typedMolecule.getMoleculePath()  == molecule_path

    assert typedMolecule.getForcefieldContent() == potentialContent
    assert typedMolecule.getForcefieldPath() == forcefieldPath


def test_moleculeToDict():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(molecule_path, forcefieldPath)

    result = typedMolecule.to_dict()

    assert result["class"] == "ReaxTypedMolecularSystem"
    assert result["electrostaticMethod"] == ElectrostaticMethod.QEQ.value
    assert result["forcefieldPath"] == Path(str(forcefieldPath))
    assert result["molecule_path"] == Path(str(molecule_path))
    assert result["moleculeFormat"] == MoleculeFileFormat.XYZ.value
    assert result["forcefieldContent"] == typedMolecule.getForcefieldContent()
    assert result["molecule_content"] == typedMolecule.getMoleculeContent()

def test_moleculeToDictToMolecule():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(molecule_path, forcefieldPath)

    dict1 = typedMolecule.to_dict()

    typedMolecule2 = ReaxTypedMolecularSystem()
    typedMolecule2.from_dict(dict1, 0)

    assert typedMolecule.to_dict() == typedMolecule2.to_dict()

def test_moleculeToJobFolder():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(molecule_path, forcefieldPath)

    job_folder = Path(tempfile.gettempdir()) / str(uuid4())
    os.makedirs(job_folder)

    moleculeHolder = typedMolecule.generateLammpsDataFile(job_folder)
    inputPath = typedMolecule.generateLammpsInputFile(job_folder, moleculeHolder)

    assert moleculeHolder is not None
    assert inputPath == job_folder / "lammps.input"
    assert (job_folder / "molecule.XYZ").is_file()
    assert (job_folder / typedMolecule.getLammpsDataFileName()).is_file()
    assert (job_folder / "model.data").is_file()
    assert (job_folder / "model.data.temp").is_file()

    shutil.rmtree(job_folder, ignore_errors=True)
