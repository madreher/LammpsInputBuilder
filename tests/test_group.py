import pytest 

from lammpsinputbuilder.group import *

def test_AllGroup():
    grp = AllGroup()
    assert grp.get_group_name() == "all"
    assert grp.add_do_commands() == ""
    assert grp.add_undo_commands() == ""

    obj_dict = grp.to_dict()
    assert obj_dict["id_name"] == "all"
    assert obj_dict["class_name"] == "AllGroup"

    grp2 = AllGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "all"
    assert grp2.add_do_commands() == ""
    assert grp2.add_undo_commands() == ""

def test_EmptyGroup():
    grp  = EmptyGroup()
    assert grp.get_group_name() == "empty"
    assert grp.add_do_commands() == ""
    assert grp.add_undo_commands() == ""

    obj_dict = grp.to_dict()
    assert obj_dict["id_name"] == "empty"
    assert obj_dict["class_name"] == "EmptyGroup"

    grp2 = EmptyGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "empty"
    assert grp2.add_do_commands() == ""
    assert grp2.add_undo_commands() == ""

def test_IndicesGroup():
    grp = IndicesGroup( group_name="myIndicesGroup", indices=[1, 2, 3])
    assert grp.get_group_name() == "myIndicesGroup"
    assert grp.get_indices() == [1, 2, 3]
    assert grp.add_do_commands() == "group myIndicesGroup id 1 2 3\n"
    assert grp.add_undo_commands() == "group myIndicesGroup delete\n"

    obj_dict = grp.to_dict()
    assert obj_dict["id_name"] == "myIndicesGroup"
    assert obj_dict["indices"] == [1, 2, 3]
    assert obj_dict["class_name"] == "IndicesGroup"

    grp2 = IndicesGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "myIndicesGroup"
    assert grp2.get_indices() == [1, 2, 3]
    assert grp2.add_do_commands() == "group myIndicesGroup id 1 2 3\n"
    assert grp2.add_undo_commands() == "group myIndicesGroup delete\n"

    grp3 = IndicesGroup( group_name="myEmptyGroup", indices=[])
    assert grp3.add_do_commands() == "group myEmptyGroup empty\n"
    assert grp3.add_undo_commands() == "group myEmptyGroup delete\n"

def test_OperationGroup():
    otherGrp1 = IndicesGroup( group_name="myOtherGroup1", indices=[1, 2, 3])
    otherGrp2 = IndicesGroup( group_name="myOtherGroup2", indices=[4, 5, 6])
    grp = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.UNION, other_groups=[otherGrp1, otherGrp2])

    assert grp.get_group_name() == "myOperationGroup"
    assert grp.get_operation() == OperationGroupEnum.UNION
    assert grp.get_other_groups()[0] == "myOtherGroup1"
    assert grp.get_other_groups()[1] == "myOtherGroup2"
    assert grp.add_do_commands() == "group myOperationGroup union myOtherGroup1 myOtherGroup2\n"
    assert grp.add_undo_commands() == "group myOperationGroup delete\n"

    obj_dict = grp.to_dict()
    assert obj_dict["id_name"] == "myOperationGroup"
    assert obj_dict["op"] == OperationGroupEnum.UNION.value
    assert obj_dict["other_groups_name"][0] == "myOtherGroup1"
    assert obj_dict["other_groups_name"][1] == "myOtherGroup2"
    assert obj_dict["class_name"] == "OperationGroup"

    grp2 = OperationGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "myOperationGroup"
    assert grp2.get_operation() == OperationGroupEnum.UNION
    assert grp2.get_other_groups()[0] == "myOtherGroup1"
    assert grp2.get_other_groups()[1] == "myOtherGroup2"

    grp = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.SUBTRACT, other_groups=[otherGrp1, otherGrp2])
    assert grp.add_do_commands() == "group myOperationGroup subtract myOtherGroup1 myOtherGroup2\n"
    grp = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.INTERSECT, other_groups=[otherGrp1, otherGrp2])
    assert grp.add_do_commands() == "group myOperationGroup intersect myOtherGroup1 myOtherGroup2\n"


    with pytest.raises(ValueError):
        grp3 = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.SUBTRACT, other_groups=[])

    with pytest.raises(ValueError):
        grp4 = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.INTERSECT, other_groups=[])

    with pytest.raises(ValueError):
        grp5 = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.UNION, other_groups=[])

def test_ManualGroup():
    grp = ManualGroup( group_name="myManualGroup", do_cmd="my_do_cmd", undo_cmd="my_undo_cmd")

    assert grp.get_group_name() == "myManualGroup"
    assert grp.get_do_cmd() == "my_do_cmd"
    assert grp.get_undo_cmd() == "my_undo_cmd"

    assert grp.add_do_commands() == "my_do_cmd\n"
    assert grp.add_undo_commands() == "my_undo_cmd\n"

    obj_dict = grp.to_dict()
    assert obj_dict["id_name"] == "myManualGroup"
    assert obj_dict["do_cmd"] == "my_do_cmd"
    assert obj_dict["undo_cmd"] == "my_undo_cmd"
    assert obj_dict["class_name"] == "ManualGroup"

    grp2 = ManualGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "myManualGroup"
    assert grp2.get_do_cmd() == "my_do_cmd"
    assert grp2.get_undo_cmd() == "my_undo_cmd"

def test_wrong_name():
    with pytest.raises(ValueError):
        obj = ManualGroup( group_name="&&&", do_cmd="my_do_cmd", undo_cmd="my_undo_cmd")
        del obj
