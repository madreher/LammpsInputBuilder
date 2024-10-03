from pathlib import Path

import pytest

from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, \
    ThermoFileIO, ManualFileIO
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.group import AllGroup

def test_DumpTrajectoryFileIO():
    obj = DumpTrajectoryFileIO(fileio_name="testFile", user_fields=["a", "b", "c", "element"], add_default_fields=True, interval=10, group=AllGroup())
    assert obj.get_fileio_name() == "testFile"
    assert obj.get_user_fields() == ["a", "b", "c", "element"]
    assert obj.get_add_default_fields() is True
    assert obj.get_default_fields() == ["id", "type", "x", "y", "z"]
    assert obj.get_interval() == 10
    assert obj.get_group_name() == AllGroup().get_group_name()

    dict_obj = obj.to_dict()
    assert dict_obj["class_name"] == "DumpTrajectoryFileIO"
    assert dict_obj["id_name"] == "testFile"
    assert dict_obj["user_fields"] == ["a", "b", "c", "element"]
    assert dict_obj["add_default_fields"] is True
    assert dict_obj["interval"] == 10
    assert dict_obj["group_name"] == AllGroup().get_group_name()

    obj2 = DumpTrajectoryFileIO()
    obj2.from_dict(dict_obj, version=0)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_user_fields() == ["a", "b", "c", "element"]
    assert obj2.get_add_default_fields() is True
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
    assert obj.get_fileio_name() == "testFile"
    assert obj.get_interval() == 10
    assert obj.get_group_name() == AllGroup().get_group_name()

    dict_obj = obj.to_dict()
    assert dict_obj["class_name"] == "ReaxBondFileIO"
    assert dict_obj["id_name"] == "testFile"
    assert dict_obj["interval"] == 10
    assert dict_obj["group_name"] == AllGroup().get_group_name()

    obj2 = ReaxBondFileIO()
    obj2.from_dict(dict_obj, version=0)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_interval() == 10
    assert obj2.get_group_name() == AllGroup().get_group_name()

    info = GlobalInformation()
    assert obj.add_do_commands(info) == "fix testFile all reaxff/bonds 10 bonds.testFile.txt\n"
    assert obj.add_undo_commands() == "unfix testFile\n"

def test_ThermoFileIO():
    obj = ThermoFileIO(fileio_name="testFile", add_default_fields=True, interval=10, user_fields=["a", "b", "c"])
    assert obj.get_fileio_name() == "testFile"
    assert obj.get_add_default_fields() is True
    assert obj.get_default_fields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj.get_interval() == 10
    assert obj.get_user_fields() == ["a", "b", "c"]

    dict_obj = obj.to_dict()
    assert dict_obj["class_name"] == "ThermoFileIO"
    assert dict_obj["id_name"] == "testFile"
    assert dict_obj["add_default_fields"] is True
    assert dict_obj["interval"] == 10
    assert dict_obj["user_fields"] == ["a", "b", "c"]

    obj2 = ThermoFileIO()
    obj2.from_dict(dict_obj, version=0)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_add_default_fields() is True
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
    assert obj.get_fileio_name() == "testFile"
    assert obj.get_do_cmd() == "startFile"
    assert obj.get_undo_cmd() == "endFile"
    assert obj.get_associated_file_path() == Path("testfile")

    dict_obj = obj.to_dict()
    assert dict_obj["class_name"] == "ManualFileIO"
    assert dict_obj["id_name"] == "testFile"
    assert dict_obj["do_cmd"] == "startFile"
    assert dict_obj["undo_cmd"] == "endFile"
    assert dict_obj["associated_file_path"] == "testfile"

    obj2 = ManualFileIO()
    obj2.from_dict(dict_obj, version=0)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_do_cmd() == "startFile"
    assert obj2.get_undo_cmd() == "endFile"
    assert obj2.get_associated_file_path() == Path("testfile")

    info = GlobalInformation()
    assert obj.add_do_commands(info) == "startFile\n"
    assert obj.add_undo_commands() == "endFile\n"

def test_wrong_name():
    with pytest.raises(ValueError):
        obj = ReaxBondFileIO(fileio_name="&&&", interval=10, group=AllGroup())
        del obj

