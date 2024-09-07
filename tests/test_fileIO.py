from lammpsinputbuilder.fileIO import *

def test_DumpTrajectoryFileIO():
    obj = DumpTrajectoryFileIO(fileIOName="testFile", userFields=["a", "b", "c"], addDefaultFields=True, interval=10, group=AllGroup())
    assert obj.getFileIOName() == "testFile"
    assert obj.getUserFields() == ["a", "b", "c"]
    assert obj.getAddDefaultFields() == True
    assert obj.getDefaultFields() == ["id", "type", "x", "y", "z"]
    assert obj.getInterval() == 10
    assert obj.getGroupName() == AllGroup().getGroupName()

    dictObj = obj.toDict()
    assert dictObj["class"] == "DumpTrajectoryFileIO"
    assert dictObj["fileIOName"] == "testFile"
    assert dictObj["userFields"] == ["a", "b", "c"]
    assert dictObj["addDefaultFields"] == True
    assert dictObj["interval"] == 10
    assert dictObj["groupName"] == AllGroup().getGroupName()

    obj2 = DumpTrajectoryFileIO()
    obj2.fromDict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getUserFields() == ["a", "b", "c"]
    assert obj2.getAddDefaultFields() == True
    assert obj2.getDefaultFields() == ["id", "type", "x", "y", "z"]
    assert obj2.getInterval() == 10
    assert obj2.getGroupName() == AllGroup().getGroupName()

    doCmd = obj.addDoCommands()
    cmds = doCmd.splitlines()
    assert cmds[0] == "dump testFile all custom 10 dump.testFile.lammpstrj id type x y z a b c"
    assert cmds[1] == "dump_modify testFile sort id"
    undoCmd = obj.addUndoCommands()
    assert undoCmd == "undump testFile\n"

def test_ReaxBondFileIO():
    obj = ReaxBondFileIO(fileIOName="testFile", interval=10, group=AllGroup())
    assert obj.getFileIOName() == "testFile"
    assert obj.getInterval() == 10
    assert obj.getGroupName() == AllGroup().getGroupName()

    dictObj = obj.toDict()
    assert dictObj["class"] == "ReaxBondFileIO"
    assert dictObj["fileIOName"] == "testFile"
    assert dictObj["interval"] == 10
    assert dictObj["groupName"] == AllGroup().getGroupName()

    obj2 = ReaxBondFileIO()
    obj2.fromDict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getInterval() == 10
    assert obj2.getGroupName() == AllGroup().getGroupName()

    assert obj.addDoCommands() == "fix testFile all reaxff/bonds 10 bonds.testFile.txt\n"
    assert obj.addUndoCommands() == "unfix testFile\n"

def test_ThermoFileIO():
    obj = ThermoFileIO(fileIOName="testFile", addDefaultFields=True, interval=10, userFields=["a", "b", "c"])
    assert obj.getFileIOName() == "testFile"
    assert obj.getAddDefaultFields() == True
    assert obj.getDefaultFields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj.getInterval() == 10
    assert obj.getUserFields() == ["a", "b", "c"]

    dictObj = obj.toDict()
    assert dictObj["class"] == "ThermoFileIO"
    assert dictObj["fileIOName"] == "testFile"
    assert dictObj["addDefaultFields"] == True
    assert dictObj["interval"] == 10
    assert dictObj["userFields"] == ["a", "b", "c"]

    obj2 = ThermoFileIO()
    obj2.fromDict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getAddDefaultFields() == True
    assert obj2.getDefaultFields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj2.getInterval() == 10
    assert obj2.getUserFields() == ["a", "b", "c"]

    cmds = obj.addDoCommands().splitlines()
    assert cmds[0] == "thermo 10"
    assert cmds[1] == "thermo_style custom step temp pe ke etotal press a b c"
    assert obj.addUndoCommands() == ""


