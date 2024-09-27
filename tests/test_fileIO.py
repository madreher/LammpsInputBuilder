from lammpsinputbuilder.fileIO import *
from lammpsinputbuilder.types import GlobalInformation

def test_DumpTrajectoryFileIO():
    obj = DumpTrajectoryFileIO(fileio_name="testFile", userFields=["a", "b", "c", "element"], addDefaultFields=True, interval=10, group=AllGroup())
    assert obj.getFileIOName() == "testFile"
    assert obj.getUserFields() == ["a", "b", "c", "element"]
    assert obj.getAddDefaultFields() == True
    assert obj.getDefaultFields() == ["id", "type", "x", "y", "z"]
    assert obj.getInterval() == 10
    assert obj.get_group_name() == AllGroup().get_group_name()

    dictObj = obj.to_dict()
    assert dictObj["class"] == "DumpTrajectoryFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["userFields"] == ["a", "b", "c", "element"]
    assert dictObj["addDefaultFields"] == True
    assert dictObj["interval"] == 10
    assert dictObj["group_name"] == AllGroup().get_group_name()

    obj2 = DumpTrajectoryFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getUserFields() == ["a", "b", "c", "element"]
    assert obj2.getAddDefaultFields() == True
    assert obj2.getDefaultFields() == ["id", "type", "x", "y", "z"]
    assert obj2.getInterval() == 10
    assert obj2.get_group_name() == AllGroup().get_group_name()

    info = GlobalInformation()
    info.setElementTable({1: "H"})
    doCmd = obj.add_do_commands(info)
    cmds = doCmd.splitlines()
    assert cmds[0] == "dump testFile all custom 10 dump.testFile.lammpstrj id type x y z a b c element"
    assert cmds[1] == "dump_modify testFile sort id"
    assert cmds[2] == "dump_modify testFile element H"
    undoCmd = obj.add_undo_commands()
    assert undoCmd == "undump testFile\n"

def test_ReaxBondFileIO():
    obj = ReaxBondFileIO(fileio_name="testFile", interval=10, group=AllGroup())
    assert obj.getFileIOName() == "testFile"
    assert obj.getInterval() == 10
    assert obj.get_group_name() == AllGroup().get_group_name()

    dictObj = obj.to_dict()
    assert dictObj["class"] == "ReaxBondFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["interval"] == 10
    assert dictObj["group_name"] == AllGroup().get_group_name()

    obj2 = ReaxBondFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getInterval() == 10
    assert obj2.get_group_name() == AllGroup().get_group_name()

    info = GlobalInformation()
    assert obj.add_do_commands(info) == "fix testFile all reaxff/bonds 10 bonds.testFile.txt\n"
    assert obj.add_undo_commands() == "unfix testFile\n"

def test_ThermoFileIO():
    obj = ThermoFileIO(fileio_name="testFile", addDefaultFields=True, interval=10, userFields=["a", "b", "c"])
    assert obj.getFileIOName() == "testFile"
    assert obj.getAddDefaultFields() == True
    assert obj.getDefaultFields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj.getInterval() == 10
    assert obj.getUserFields() == ["a", "b", "c"]

    dictObj = obj.to_dict()
    assert dictObj["class"] == "ThermoFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["addDefaultFields"] == True
    assert dictObj["interval"] == 10
    assert dictObj["userFields"] == ["a", "b", "c"]

    obj2 = ThermoFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getAddDefaultFields() == True
    assert obj2.getDefaultFields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj2.getInterval() == 10
    assert obj2.getUserFields() == ["a", "b", "c"]

    info = GlobalInformation()
    cmds = obj.add_do_commands(info).splitlines()
    assert cmds[0] == "thermo 10"
    assert cmds[1] == "thermo_style custom step temp pe ke etotal press a b c"
    assert obj.add_undo_commands() == ""

def test_ManualFileIO():
    obj = ManualFileIO(fileio_name="testFile", doCmd="startFile", undoCmd="endFile", associatedFilePath="testfile")
    assert obj.getFileIOName() == "testFile"
    assert obj.getDoCmd() == "startFile"
    assert obj.getUndoCmd() == "endFile"
    assert obj.getAssociatedFilePath() == Path("testfile")

    dictObj = obj.to_dict()
    assert dictObj["class"] == "ManualFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["doCmd"] == "startFile"
    assert dictObj["undoCmd"] == "endFile"
    assert dictObj["associatedFilePath"] == "testfile"

    obj2 = ManualFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.getDoCmd() == "startFile"
    assert obj2.getUndoCmd() == "endFile"
    assert obj2.getAssociatedFilePath() == Path("testfile")

    info = GlobalInformation()
    assert obj.add_do_commands(info) == "startFile\n"
    assert obj.add_undo_commands() == "endFile\n"


