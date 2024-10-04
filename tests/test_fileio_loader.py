from pathlib import Path

import pytest

from lammpsinputbuilder.loader.fileio_loader import FileIOLoader
from lammpsinputbuilder.fileio import ReaxBondFileIO, DumpTrajectoryFileIO, \
    ThermoFileIO, ManualFileIO
from lammpsinputbuilder.group import AllGroup

def test_load_reax_bond_fileio():
    obj = ReaxBondFileIO(fileio_name="testFile", interval=10, group=AllGroup())
    obj_dict = obj.to_dict()

    loader = FileIOLoader()
    obj2 = loader.dict_to_fileio(obj_dict, version=0)
    assert isinstance(obj2, ReaxBondFileIO)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_interval() == 10
    assert obj2.get_group_name() == AllGroup().get_group_name()

def test_load_dump_trajectory_fileio():
    obj = DumpTrajectoryFileIO(
        fileio_name="testFile", 
        user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup())
    obj_dict = obj.to_dict()

    loader = FileIOLoader()
    obj2 = loader.dict_to_fileio(obj_dict, version=0)
    assert isinstance(obj2, DumpTrajectoryFileIO)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_user_fields() == ["a", "b", "c", "element"]
    assert obj2.get_add_default_fields() is True
    assert obj2.get_default_fields() == ["id", "type", "x", "y", "z"]

def test_load_thermo_fileio():
    obj = ThermoFileIO(
        fileio_name="testFile",
        add_default_fields=True,
        interval=10,
        user_fields=["a", "b", "c"])
    obj_dict = obj.to_dict()

    loader = FileIOLoader()
    obj2 = loader.dict_to_fileio(obj_dict, version=0)
    assert isinstance(obj2, ThermoFileIO)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_add_default_fields() is True
    assert obj2.get_default_fields() == ["step", "temp", "pe", "ke", "etotal", "press"]
    assert obj2.get_interval() == 10
    assert obj2.get_user_fields() == ["a", "b", "c"]

def test_load_manual_fileio():
    obj = ManualFileIO(
        fileio_name="testFile",
        do_cmd="startFile",
        undo_cmd="endFile",
        associated_file_path="testfile")
    obj_dict = obj.to_dict()

    loader = FileIOLoader()
    obj2 = loader.dict_to_fileio(obj_dict, version=0)
    assert isinstance(obj2, ManualFileIO)
    assert obj2.get_fileio_name() == "testFile"
    assert obj2.get_do_cmd() == "startFile"
    assert obj2.get_undo_cmd() == "endFile"
    assert obj2.get_associated_file_path() == Path("testfile")

def test_load_no_class_fileio():
    obj = ManualFileIO(
        fileio_name="testFile",
        do_cmd="startFile",
        undo_cmd="endFile",
        associated_file_path="testfile")

    obj_dict = obj.to_dict()
    del obj_dict["class_name"]

    with pytest.raises(RuntimeError):
        loader = FileIOLoader()
        obj2 = loader.dict_to_fileio(obj_dict, version=0)
        del obj2


def test_load_unknown_class_fileio():
    obj = ManualFileIO(
        fileio_name="testFile",
        do_cmd="startFile",
        undo_cmd="endFile",
        associated_file_path="testfile")

    obj_dict = obj.to_dict()
    obj_dict["class_name"] = "unknown"

    with pytest.raises(RuntimeError):
        loader = FileIOLoader()
        obj2 = loader.dict_to_fileio(obj_dict, version=0)
        del obj2