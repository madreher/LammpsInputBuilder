import json
from pathlib import Path

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, \
    MoleculeFileFormat
from lammpsinputbuilder.typedmolecule import AireboTypedMolecularSystem

from lammpsinputbuilder.model.typedmolecule_model import AireboTypedMolecularSystemModel


def test_airebo_molecule_model():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / \
        'data' / 'models' / 'benzene.xyz'
    forcefield_path = Path(__file__).parent.parent / \
        'data' / 'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    obj_dict = typed_molecule.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    obj_model1 = AireboTypedMolecularSystemModel.model_validate_json(
        obj_dict_str)
    assert obj_model1.class_name == "AireboTypedMolecularSystem"
    assert obj_model1.bbox_style == BoundingBoxStyle.PERIODIC.value
    assert obj_model1.electrostatic_method == ElectrostaticMethod.QEQ.value
    assert obj_model1.forcefield_name == "CH.airebo"
    assert obj_model1.molecule_name == "benzene.xyz"
    assert obj_model1.molecule_format == MoleculeFileFormat.XYZ.value
    assert obj_model1.forcefield_content == typed_molecule.get_forcefield_content()
    assert obj_model1.molecule_content == typed_molecule.get_molecule_content()

    obj_model2 = AireboTypedMolecularSystemModel(**obj_dict)
    assert obj_model2.class_name == "AireboTypedMolecularSystem"
    assert obj_model2.bbox_style == BoundingBoxStyle.PERIODIC.value
    assert obj_model2.electrostatic_method == ElectrostaticMethod.QEQ.value
    assert obj_model2.forcefield_name == "CH.airebo"
    assert obj_model2.molecule_name == "benzene.xyz"
    assert obj_model2.molecule_format == MoleculeFileFormat.XYZ.value
    assert obj_model2.forcefield_content == typed_molecule.get_forcefield_content()
    assert obj_model2.molecule_content == typed_molecule.get_molecule_content()
