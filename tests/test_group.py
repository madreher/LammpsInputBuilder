import pytest 

from lammpsinputbuilder.group import AllGroup, EmptyGroup,IndicesGroup, OperationGroup, OperationGroupEnum

def test_AllGroup():
    grp = AllGroup()
    assert grp.getGroupName() == "all"
    assert grp.addDoCommands() == ""
    assert grp.addUndoCommands() == ""

    objDict = grp.toDict()
    assert objDict["groupName"] == "all"
    assert objDict["class"] == "AllGroup"

    grp2 = AllGroup()
    grp2.fromDict(objDict, version=0)
    assert grp2.getGroupName() == "all"
    assert grp2.addDoCommands() == ""
    assert grp2.addUndoCommands() == ""

def test_EmptyGroup():
    grp  = EmptyGroup()
    assert grp.getGroupName() == "empty"
    assert grp.addDoCommands() == ""
    assert grp.addUndoCommands() == ""

    objDict = grp.toDict()
    assert objDict["groupName"] == "empty"
    assert objDict["class"] == "EmptyGroup"

    grp2 = EmptyGroup()
    grp2.fromDict(objDict, version=0)
    assert grp2.getGroupName() == "empty"
    assert grp2.addDoCommands() == ""
    assert grp2.addUndoCommands() == ""

def test_IndicesGroup():
    grp = IndicesGroup( groupName="myIndicesGroup", indices=[1, 2, 3])
    assert grp.getGroupName() == "myIndicesGroup"
    assert grp.getIndices() == [1, 2, 3]
    assert grp.addDoCommands() == "group myIndicesGroup id 1 2 3\n"
    assert grp.addUndoCommands() == "group myIndicesGroup delete\n"

    objDict = grp.toDict()
    assert objDict["groupName"] == "myIndicesGroup"
    assert objDict["indices"] == [1, 2, 3]
    assert objDict["class"] == "IndicesGroup"

    grp2 = IndicesGroup()
    grp2.fromDict(objDict, version=0)
    assert grp2.getGroupName() == "myIndicesGroup"
    assert grp2.getIndices() == [1, 2, 3]
    assert grp2.addDoCommands() == "group myIndicesGroup id 1 2 3\n"
    assert grp2.addUndoCommands() == "group myIndicesGroup delete\n"

    grp3 = IndicesGroup( groupName="myEmptyGroup", indices=[])
    assert grp3.addDoCommands() == "group myEmptyGroup empty\n"
    assert grp3.addUndoCommands() == "group myEmptyGroup delete\n"

def test_OperationGroup():
    otherGrp1 = IndicesGroup( groupName="myOtherGroup1", indices=[1, 2, 3])
    otherGrp2 = IndicesGroup( groupName="myOtherGroup2", indices=[4, 5, 6])
    grp = OperationGroup( groupName="myOperationGroup", op = OperationGroupEnum.UNION, otherGroups=[otherGrp1, otherGrp2])

    assert grp.getGroupName() == "myOperationGroup"
    assert grp.getOperation() == OperationGroupEnum.UNION
    assert grp.getOtherGroups()[0] == "myOtherGroup1"
    assert grp.getOtherGroups()[1] == "myOtherGroup2"
    assert grp.addDoCommands() == "group myOperationGroup union myOtherGroup1 myOtherGroup2\n"
    assert grp.addUndoCommands() == "group myOperationGroup delete\n"

    objDict = grp.toDict()
    assert objDict["groupName"] == "myOperationGroup"
    assert objDict["op"] == OperationGroupEnum.UNION.value
    assert objDict["otherGroups"][0] == "myOtherGroup1"
    assert objDict["otherGroups"][1] == "myOtherGroup2"
    assert objDict["class"] == "OperationGroup"

    grp2 = OperationGroup()
    grp2.fromDict(objDict, version=0)
    assert grp2.getGroupName() == "myOperationGroup"
    assert grp2.getOperation() == OperationGroupEnum.UNION
    assert grp2.getOtherGroups()[0] == "myOtherGroup1"
    assert grp2.getOtherGroups()[1] == "myOtherGroup2"

    grp = OperationGroup( groupName="myOperationGroup", op = OperationGroupEnum.SUBTRACT, otherGroups=[otherGrp1, otherGrp2])
    assert grp.addDoCommands() == "group myOperationGroup subtract myOtherGroup1 myOtherGroup2\n"
    grp = OperationGroup( groupName="myOperationGroup", op = OperationGroupEnum.INTERSECT, otherGroups=[otherGrp1, otherGrp2])
    assert grp.addDoCommands() == "group myOperationGroup intersect myOtherGroup1 myOtherGroup2\n"


    with pytest.raises(ValueError):
        grp3 = OperationGroup( groupName="myOperationGroup", op = OperationGroupEnum.SUBTRACT, otherGroups=[])

    with pytest.raises(ValueError):
        grp4 = OperationGroup( groupName="myOperationGroup", op = OperationGroupEnum.INTERSECT, otherGroups=[])

    with pytest.raises(ValueError):
        grp5 = OperationGroup( groupName="myOperationGroup", op = OperationGroupEnum.UNION, otherGroups=[])
