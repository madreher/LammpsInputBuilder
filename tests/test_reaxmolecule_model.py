import json
from pathlib import Path

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, \
    MoleculeFileFormat
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem

from lammpsinputbuilder.model.typedmolecule_model import ReaxTypedMolecularSystemModel


def test_reax_molecule_model():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / \
        'data' / 'models' / 'benzene.xyz'
    forcefield_path = Path(__file__).parent.parent / \
        'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typed_molecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    obj_dict = typed_molecule.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    obj_model1 = ReaxTypedMolecularSystemModel.model_validate_json(
        obj_dict_str)
    assert obj_model1.class_name == "ReaxTypedMolecularSystem"
    assert obj_model1.bbox_style == BoundingBoxStyle.PERIODIC.value
    assert obj_model1.electrostatic_method == ElectrostaticMethod.QEQ.value
    assert obj_model1.forcefield_name == "ffield.reax.Fe_O_C_H.reax"
    assert obj_model1.molecule_name == "benzene.xyz"
    assert obj_model1.molecule_format == MoleculeFileFormat.XYZ.value
    assert obj_model1.forcefield_content == typed_molecule.get_forcefield_content()
    assert obj_model1.molecule_content == typed_molecule.get_molecule_content()

    obj_model2 = ReaxTypedMolecularSystemModel(**obj_dict)
    assert obj_model2.class_name == "ReaxTypedMolecularSystem"
    assert obj_model2.bbox_style == BoundingBoxStyle.PERIODIC.value
    assert obj_model2.electrostatic_method == ElectrostaticMethod.QEQ.value
    assert obj_model2.forcefield_name == "ffield.reax.Fe_O_C_H.reax"
    assert obj_model2.molecule_name == "benzene.xyz"
    assert obj_model2.molecule_format == MoleculeFileFormat.XYZ.value
    assert obj_model2.forcefield_content == typed_molecule.get_forcefield_content()
    assert obj_model2.molecule_content == typed_molecule.get_molecule_content()
