import json 

from lammpsinputbuilder.fileio import ReaxBondFileIO, DumpTrajectoryFileIO, \
    ThermoFileIO, ManualFileIO
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.model.fileio_model import ReaxBondFileIOModel, \
    DumpTrajectoryModel, ThermoFileIOModel, ManualFileIOModel

def test_reaxbond_fileio_model():
    obj = ReaxBondFileIO(fileio_name="testFile", interval=10, group=AllGroup())

    dict_obj = obj.to_dict()
    dict_obj_str = json.dumps(dict_obj)

    obj_model1 = ReaxBondFileIOModel.model_validate_json(dict_obj_str)
    assert obj_model1.class_name == "ReaxBondFileIO"
    assert obj_model1.id_name == "testFile"
    assert obj_model1.interval == 10

    obj_model2 = ReaxBondFileIOModel(**dict_obj)
    assert obj_model2.class_name == "ReaxBondFileIO"
    assert obj_model2.id_name == "testFile"
    assert obj_model2.interval == 10

def test_dump_trajectory_fileio_model():
    obj = DumpTrajectoryFileIO(
        fileio_name="testFile",
        user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup())
    
    dict_obj = obj.to_dict()
    dict_obj_str = json.dumps(dict_obj)

    obj_model1 = DumpTrajectoryModel.model_validate_json(dict_obj_str)
    assert obj_model1.class_name == "DumpTrajectoryFileIO"
    assert obj_model1.id_name == "testFile"
    assert obj_model1.user_fields == ["a", "b", "c", "element"]
    assert obj_model1.add_default_fields is True
    assert obj_model1.interval == 10

    obj_model2 = DumpTrajectoryModel(**dict_obj)
    assert obj_model2.class_name == "DumpTrajectoryFileIO"
    assert obj_model2.id_name == "testFile"
    assert obj_model2.user_fields == ["a", "b", "c", "element"]
    assert obj_model2.add_default_fields is True
    assert obj_model2.interval == 10

def test_thermo_fileio_model():
    obj = ThermoFileIO(
        fileio_name="testFile",
        add_default_fields=True,
        interval=10,
        user_fields=["a", "b", "c"])

    dict_obj = obj.to_dict()
    dict_obj_str = json.dumps(dict_obj)

    obj_model1 = ThermoFileIOModel.model_validate_json(dict_obj_str)
    assert obj_model1.class_name == "ThermoFileIO"
    assert obj_model1.id_name == "testFile"
    assert obj_model1.add_default_fields is True
    assert obj_model1.interval == 10
    assert obj_model1.user_fields == ["a", "b", "c"]

    obj_model2 = ThermoFileIOModel(**dict_obj)
    assert obj_model2.class_name == "ThermoFileIO"
    assert obj_model2.id_name == "testFile"
    assert obj_model2.add_default_fields is True
    assert obj_model2.interval == 10
    assert obj_model2.user_fields == ["a", "b", "c"]

def test_manual_fileio_model():
    obj = ManualFileIO(
        fileio_name="testFile",
        do_cmd="my_do_cmd",
        undo_cmd="my_undo_cmd",
        associated_file_path="testfile")

    dict_obj = obj.to_dict()
    dict_obj_str = json.dumps(dict_obj)

    obj_model1 = ManualFileIOModel.model_validate_json(dict_obj_str)
    assert obj_model1.class_name == "ManualFileIO"
    assert obj_model1.id_name == "testFile"
    assert obj_model1.do_cmd == "my_do_cmd"
    assert obj_model1.undo_cmd == "my_undo_cmd"
    assert obj_model1.associated_file_path == "testfile"

    obj_model2 = ManualFileIOModel(**dict_obj)
    assert obj_model2.class_name == "ManualFileIO"
    assert obj_model2.id_name == "testFile"
    assert obj_model2.do_cmd == "my_do_cmd"
    assert obj_model2.undo_cmd == "my_undo_cmd"
    assert obj_model2.associated_file_path == "testfile"
