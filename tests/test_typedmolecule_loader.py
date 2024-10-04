from pathlib import Path

import pytest

from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, MoleculeFileFormat
from lammpsinputbuilder.loader.typedmolecule_loader import TypedMolecularSystemLoader
from lammpsinputbuilder.group import AllGroup

def test_load_reax_typed_molecular_system_empty():
    obj = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.SHRINK,
        electrostatic_method=ElectrostaticMethod.ACKS2
    )
    obj_dict = obj.to_dict()

    loader = TypedMolecularSystemLoader()
    obj2 = loader.dict_to_typed_molecular_system(obj_dict)
    assert isinstance(obj2, ReaxTypedMolecularSystem)
    assert obj2.get_boundingbox_style() == BoundingBoxStyle.SHRINK
    assert obj2.get_electrostatic_method() == ElectrostaticMethod.ACKS2
    assert obj2.is_model_loaded() is False
    assert obj2.get_ase_model() is None
    assert obj2.get_molecule_content() == ""
    assert obj2.get_forcefield_content() == ""
    assert obj2.get_forcefield_name() is None
    assert obj2.get_molecule_name() is None
    assert obj2.get_molecule_format() is None


def test_load_reax_typed_molecular_system():
    obj = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.SHRINK,
        electrostatic_method=ElectrostaticMethod.ACKS2
    )

    model_data = Path(__file__).parent.parent / 'data' / \
        'models' / 'benzene.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / \
        'potentials' / 'Si_C_H.reax'

    obj.load_from_file(model_data, forcefield)

    obj_dict = obj.to_dict()

    loader = TypedMolecularSystemLoader()
    obj2 = loader.dict_to_typed_molecular_system(obj_dict)
    assert isinstance(obj2, ReaxTypedMolecularSystem)
    assert obj2.get_boundingbox_style() == BoundingBoxStyle.SHRINK
    assert obj2.get_electrostatic_method() == ElectrostaticMethod.ACKS2
    assert obj2.is_model_loaded() is True
    assert obj2.get_ase_model() is not None
    assert len(obj2.get_ase_model().get_positions()) == 12
    assert obj2.get_molecule_content() == model_data.read_text()
    assert obj2.get_forcefield_content() == forcefield.read_text()
    assert obj2.get_forcefield_name() == Path(forcefield.name)
    assert obj2.get_molecule_name() == Path(model_data.name)
    assert obj2.get_molecule_format() == MoleculeFileFormat.XYZ

def test_load_no_class_typed_molecular_system():
    obj = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.SHRINK,
        electrostatic_method=ElectrostaticMethod.ACKS2
    )

    obj_dict = obj.to_dict()
    del obj_dict["class_name"]

    with pytest.raises(RuntimeError):
        loader = TypedMolecularSystemLoader()
        obj2 = loader.dict_to_typed_molecular_system(obj_dict)
        del obj2


def test_load_unknown_class_typed_molecular_system():
    obj = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.SHRINK,
        electrostatic_method=ElectrostaticMethod.ACKS2
    )

    obj_dict = obj.to_dict()
    obj_dict["class_name"] = 'unknown'

    with pytest.raises(RuntimeError):
        loader = TypedMolecularSystemLoader()
        obj2 = loader.dict_to_typed_molecular_system(obj_dict)
        del obj2