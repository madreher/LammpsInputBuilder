import pytest 

from lammpsinputbuilder.group import *

def test_AllGroup():
    grp = AllGroup()
    assert grp.get_group_name() == "all"
    assert grp.add_do_commands() == ""
    assert grp.add_undo_commands() == ""

    obj_dict = grp.to_dict()
    assert obj_dict["group_name"] == "all"
    assert obj_dict["class"] == "AllGroup"

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
    assert obj_dict["group_name"] == "empty"
    assert obj_dict["class"] == "EmptyGroup"

    grp2 = EmptyGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "empty"
    assert grp2.add_do_commands() == ""
    assert grp2.add_undo_commands() == ""

def test_IndicesGroup():
    grp = IndicesGroup( group_name="myIndicesGroup", indices=[1, 2, 3])
    assert grp.get_group_name() == "myIndicesGroup"
    assert grp.getIndices() == [1, 2, 3]
    assert grp.add_do_commands() == "group myIndicesGroup id 1 2 3\n"
    assert grp.add_undo_commands() == "group myIndicesGroup delete\n"

    obj_dict = grp.to_dict()
    assert obj_dict["group_name"] == "myIndicesGroup"
    assert obj_dict["indices"] == [1, 2, 3]
    assert obj_dict["class"] == "IndicesGroup"

    grp2 = IndicesGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "myIndicesGroup"
    assert grp2.getIndices() == [1, 2, 3]
    assert grp2.add_do_commands() == "group myIndicesGroup id 1 2 3\n"
    assert grp2.add_undo_commands() == "group myIndicesGroup delete\n"

    grp3 = IndicesGroup( group_name="myEmptyGroup", indices=[])
    assert grp3.add_do_commands() == "group myEmptyGroup empty\n"
    assert grp3.add_undo_commands() == "group myEmptyGroup delete\n"

def test_OperationGroup():
    otherGrp1 = IndicesGroup( group_name="myOtherGroup1", indices=[1, 2, 3])
    otherGrp2 = IndicesGroup( group_name="myOtherGroup2", indices=[4, 5, 6])
    grp = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.UNION, otherGroups=[otherGrp1, otherGrp2])

    assert grp.get_group_name() == "myOperationGroup"
    assert grp.getOperation() == OperationGroupEnum.UNION
    assert grp.getOtherGroups()[0] == "myOtherGroup1"
    assert grp.getOtherGroups()[1] == "myOtherGroup2"
    assert grp.add_do_commands() == "group myOperationGroup union myOtherGroup1 myOtherGroup2\n"
    assert grp.add_undo_commands() == "group myOperationGroup delete\n"

    obj_dict = grp.to_dict()
    assert obj_dict["group_name"] == "myOperationGroup"
    assert obj_dict["op"] == OperationGroupEnum.UNION.value
    assert obj_dict["otherGroups"][0] == "myOtherGroup1"
    assert obj_dict["otherGroups"][1] == "myOtherGroup2"
    assert obj_dict["class"] == "OperationGroup"

    grp2 = OperationGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "myOperationGroup"
    assert grp2.getOperation() == OperationGroupEnum.UNION
    assert grp2.getOtherGroups()[0] == "myOtherGroup1"
    assert grp2.getOtherGroups()[1] == "myOtherGroup2"

    grp = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.SUBTRACT, otherGroups=[otherGrp1, otherGrp2])
    assert grp.add_do_commands() == "group myOperationGroup subtract myOtherGroup1 myOtherGroup2\n"
    grp = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.INTERSECT, otherGroups=[otherGrp1, otherGrp2])
    assert grp.add_do_commands() == "group myOperationGroup intersect myOtherGroup1 myOtherGroup2\n"


    with pytest.raises(ValueError):
        grp3 = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.SUBTRACT, otherGroups=[])

    with pytest.raises(ValueError):
        grp4 = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.INTERSECT, otherGroups=[])

    with pytest.raises(ValueError):
        grp5 = OperationGroup( group_name="myOperationGroup", op = OperationGroupEnum.UNION, otherGroups=[])

def test_ManualGroup():
    grp = ManualGroup( group_name="myManualGroup", doCmd="myDoCmd", undoCmd="myUndoCmd")

    assert grp.get_group_name() == "myManualGroup"
    assert grp.getDoCmd() == "myDoCmd"
    assert grp.getUndoCmd() == "myUndoCmd"

    assert grp.add_do_commands() == "myDoCmd\n"
    assert grp.add_undo_commands() == "myUndoCmd\n"

    obj_dict = grp.to_dict()
    assert obj_dict["group_name"] == "myManualGroup"
    assert obj_dict["doCmd"] == "myDoCmd"
    assert obj_dict["undoCmd"] == "myUndoCmd"
    assert obj_dict["class"] == "ManualGroup"

    grp2 = ManualGroup()
    grp2.from_dict(obj_dict, version=0)
    assert grp2.get_group_name() == "myManualGroup"
    assert grp2.getDoCmd() == "myDoCmd"
    assert grp2.getUndoCmd() == "myUndoCmd"