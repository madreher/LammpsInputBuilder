import pytest

from lammpsinputbuilder.loader.group_loader import GroupLoader
from lammpsinputbuilder.group import AllGroup, EmptyGroup, IndicesGroup, \
    ManualGroup, OperationGroup, OperationGroupEnum, ReferenceGroup

def test_load_all_group():

    obj = AllGroup()

    obj_dict = obj.to_dict()
    loader = GroupLoader()
    obj2 = loader.dict_to_group(obj_dict)
    assert obj2.get_group_name() == "all"

def test_load_empty_group():

    obj = EmptyGroup()

    obj_dict = obj.to_dict()
    loader = GroupLoader()
    obj2 = loader.dict_to_group(obj_dict)
    assert obj2.get_group_name() == "empty"

def test_load_indices_group():

    obj = IndicesGroup(group_name="indices", indices=[1, 2, 3])

    obj_dict = obj.to_dict()
    loader = GroupLoader()
    obj2 = loader.dict_to_group(obj_dict)
    assert obj2.get_group_name() == "indices"
    assert obj2.get_indices() == [1, 2, 3]

def test_load_reference_group():
    ref = AllGroup()
    obj = ReferenceGroup(group_name="reference", reference=ref)

    obj_dict = obj.to_dict()
    loader = GroupLoader()
    obj2 = loader.dict_to_group(obj_dict)
    assert obj2.get_group_name() == "all"
    assert obj2.get_reference_name() == "all"

def test_load_operation_group():

    other_grp1 = IndicesGroup( group_name="myOtherGroup1", indices=[1, 2, 3])
    other_grp2 = IndicesGroup( group_name="myOtherGroup2", indices=[4, 5, 6])
    obj = OperationGroup( group_name="myOperationGroup",
                         op = OperationGroupEnum.UNION,
                         other_groups=[other_grp1, other_grp2])

    obj_dict = obj.to_dict()
    loader = GroupLoader()
    obj2 = loader.dict_to_group(obj_dict)
    assert obj2.get_group_name() == "myOperationGroup"
    assert obj2.get_operation() == OperationGroupEnum.UNION
    assert len(obj2.get_other_groups()) == 2
    assert obj2.get_other_groups()[0] == "myOtherGroup1"
    assert obj2.get_other_groups()[1] == "myOtherGroup2"

def test_load_manual_group():

    obj = ManualGroup(group_name="manual", do_cmd="start", undo_cmd="end")

    obj_dict = obj.to_dict()
    loader = GroupLoader()
    obj2 = loader.dict_to_group(obj_dict)
    assert obj2.get_group_name() == "manual"
    assert obj2.get_do_cmd() == "start"
    assert obj2.get_undo_cmd() == "end"

def test_load_no_class_group():

    obj = ManualGroup(group_name="manual", do_cmd="start", undo_cmd="end")

    obj_dict = obj.to_dict()
    del obj_dict["class_name"]

    with pytest.raises(RuntimeError):
        loader = GroupLoader()
        obj2 = loader.dict_to_group(obj_dict)
        del obj2

def test_load_unknown_class_group():

    obj = ManualGroup(group_name="manual", do_cmd="start", undo_cmd="end")

    obj_dict = obj.to_dict()
    obj_dict["class_name"] = "unknown"

    with pytest.raises(RuntimeError):
        loader = GroupLoader()
        obj2 = loader.dict_to_group(obj_dict)
        del obj2
