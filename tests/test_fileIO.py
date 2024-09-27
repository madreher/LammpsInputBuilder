from lammpsinputbuilder.fileIO import *
from lammpsinputbuilder.types import GlobalInformation

def test_DumpTrajectoryFileIO():
    obj = DumpTrajectoryFileIO(fileio_name="testFile", user_fields=["a", "b", "c", "element"], add_default_fields=True, interval=10, group=AllGroup())
    assert obj.getFileIOName() == "testFile"
    assert obj.get_user_fields() == ["a", "b", "c", "element"]
    assert obj.get_add_default_fields() == True
    assert obj.get_default_fields() == ["id", "type", "x", "y", "z"]
    assert obj.get_interval() == 10
    assert obj.get_group_name() == AllGroup().get_group_name()

    dictObj = obj.to_dict()
    assert dictObj["class"] == "DumpTrajectoryFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["user_fields"] == ["a", "b", "c", "element"]
    assert dictObj["add_default_fields"] == True
    assert dictObj["interval"] == 10
    assert dictObj["group_name"] == AllGroup().get_group_name()

    obj2 = DumpTrajectoryFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.get_user_fields() == ["a", "b", "c", "element"]
    assert obj2.get_add_default_fields() == True
    assert obj2.get_default_fields() == ["id", "type", "x", "y", "z"]
    assert obj2.get_interval() == 10
    assert obj2.get_group_name() == AllGroup().get_group_name()

    info = GlobalInformation()
    info.set_element_table({1: "H"})
    do_cmd = obj.add_do_commands(info)
    cmds = do_cmd.splitlines()
    assert cmds[0] == "dump testFile all custom 10 dump.testFile.lammpstrj id type x y z a b c element"
    assert cmds[1] == "dump_modify testFile sort id"
    assert cmds[2] == "dump_modify testFile element H"
    undo_cmd = obj.add_undo_commands()
    assert undo_cmd == "undump testFile\n"

def test_ReaxBondFileIO():
    obj = ReaxBondFileIO(fileio_name="testFile", interval=10, group=AllGroup())
    assert obj.getFileIOName() == "testFile"
    assert obj.get_interval() == 10
    assert obj.get_group_name() == AllGroup().get_group_name()

    dictObj = obj.to_dict()
    assert dictObj["class"] == "ReaxBondFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["interval"] == 10
    assert dictObj["group_name"] == AllGroup().get_group_name()

    obj2 = ReaxBondFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.get_interval() == 10
    assert obj2.get_group_name() == AllGroup().get_group_name()

    info = GlobalInformation()
    assert obj.add_do_commands(info) == "fix testFile all reaxff/bonds 10 bonds.testFile.txt\n"
    assert obj.add_undo_commands() == "unfix testFile\n"

def test_ThermoFileIO():
    obj = ThermoFileIO(fileio_name="testFile", add_default_fields=True, interval=10, user_fields=["a", "b", "c"])
    assert obj.getFileIOName() == "testFile"
    assert obj.get_add_default_fields() == True
    assert obj.get_default_fields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj.get_interval() == 10
    assert obj.get_user_fields() == ["a", "b", "c"]

    dictObj = obj.to_dict()
    assert dictObj["class"] == "ThermoFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["add_default_fields"] == True
    assert dictObj["interval"] == 10
    assert dictObj["user_fields"] == ["a", "b", "c"]

    obj2 = ThermoFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.get_add_default_fields() == True
    assert obj2.get_default_fields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj2.get_interval() == 10
    assert obj2.get_user_fields() == ["a", "b", "c"]

    info = GlobalInformation()
    cmds = obj.add_do_commands(info).splitlines()
    assert cmds[0] == "thermo 10"
    assert cmds[1] == "thermo_style custom step temp pe ke etotal press a b c"
    assert obj.add_undo_commands() == ""

def test_ManualFileIO():
    obj = ManualFileIO(fileio_name="testFile", do_cmd="startFile", undo_cmd="endFile", associated_file_path="testfile")
    assert obj.getFileIOName() == "testFile"
    assert obj.get_do_cmd() == "startFile"
    assert obj.get_undo_cmd() == "endFile"
    assert obj.get_associated_file_path() == Path("testfile")

    dictObj = obj.to_dict()
    assert dictObj["class"] == "ManualFileIO"
    assert dictObj["fileio_name"] == "testFile"
    assert dictObj["do_cmd"] == "startFile"
    assert dictObj["undo_cmd"] == "endFile"
    assert dictObj["associated_file_path"] == "testfile"

    obj2 = ManualFileIO()
    obj2.from_dict(dictObj, version=0)
    assert obj2.getFileIOName() == "testFile"
    assert obj2.get_do_cmd() == "startFile"
    assert obj2.get_undo_cmd() == "endFile"
    assert obj2.get_associated_file_path() == Path("testfile")

    info = GlobalInformation()
    assert obj.add_do_commands(info) == "startFile\n"
    assert obj.add_undo_commands() == "endFile\n"


