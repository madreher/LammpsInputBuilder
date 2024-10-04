import json 

from lammpsinputbuilder.group import AllGroup, EmptyGroup, IndicesGroup, \
    ManualGroup, OperationGroup, OperationGroupEnum, ReferenceGroup
from lammpsinputbuilder.model.group_model import AllGroupModel, EmptyGroupModel, \
    IndicesGroupModel, ManualGroupModel, OperationGroupModel, \
    ReferenceGroupModel

def test_all_group_model():
    obj = AllGroup()

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = AllGroupModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "AllGroup"
    assert obj_model1.id_name == "all"

    # Populate the model from the dictionnary
    obj_model2 = AllGroupModel(**obj_dict)
    assert obj_model2.class_name == "AllGroup"
    assert obj_model2.id_name == "all"

def test_empty_group_model():
    obj = EmptyGroup()

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = EmptyGroupModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "EmptyGroup"
    assert obj_model1.id_name == "empty"

    # Populate the model from the dictionnary
    obj_model2 = EmptyGroupModel(**obj_dict)
    assert obj_model2.class_name == "EmptyGroup"
    assert obj_model2.id_name == "empty"

def test_indices_group_model():
    obj = IndicesGroup(group_name="defaultIndicesGroup", indices=[1, 2, 3, 4, 5, 6, 7, 8, 9])

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = IndicesGroupModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "IndicesGroup"
    assert obj_model1.id_name == "defaultIndicesGroup"
    assert obj_model1.indices == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Populate the model from the dictionnary
    obj_model2 = IndicesGroupModel(**obj_dict)
    assert obj_model2.class_name == "IndicesGroup"
    assert obj_model2.id_name == "defaultIndicesGroup"
    assert obj_model2.indices == [1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_operation_group_model():
    other_grp1 = IndicesGroup( group_name="myOtherGroup1", indices=[1, 2, 3])
    other_grp2 = IndicesGroup( group_name="myOtherGroup2", indices=[4, 5, 6])
    grp = OperationGroup( group_name="myOperationGroup", 
                         op = OperationGroupEnum.UNION, other_groups=[other_grp1, other_grp2])

    obj_dict = grp.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = OperationGroupModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "OperationGroup"
    assert obj_model1.id_name == "myOperationGroup"
    assert obj_model1.op == OperationGroupEnum.UNION
    assert obj_model1.other_groups_name[0] == "myOtherGroup1"
    assert obj_model1.other_groups_name[1] == "myOtherGroup2"

    # Populate the model from the dictionnary
    obj_model2 = OperationGroupModel(**obj_dict)
    assert obj_model2.class_name == "OperationGroup"
    assert obj_model2.id_name == "myOperationGroup"
    assert obj_model2.op == OperationGroupEnum.UNION
    assert obj_model2.other_groups_name[0] == "myOtherGroup1"
    assert obj_model2.other_groups_name[1] == "myOtherGroup2"

def test_manual_group_model():
    obj = ManualGroup( group_name="myManualGroup", do_cmd="my_do_cmd", undo_cmd="my_undo_cmd")

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = ManualGroupModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "ManualGroup"
    assert obj_model1.id_name == "myManualGroup"
    assert obj_model1.do_cmd == "my_do_cmd"
    assert obj_model1.undo_cmd == "my_undo_cmd"

    # Populate the model from the dictionnary
    obj_model2 = ManualGroupModel(**obj_dict)
    assert obj_model2.class_name == "ManualGroup"
    assert obj_model2.id_name == "myManualGroup"
    assert obj_model2.do_cmd == "my_do_cmd"
    assert obj_model2.undo_cmd == "my_undo_cmd"

def test_reference_group_model():
    obj = ReferenceGroup( group_name="myReferenceGroup", reference=IndicesGroup("myReference", indices=[1, 2, 3]))

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = ReferenceGroupModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "ReferenceGroup"
    assert obj_model1.id_name == "myReferenceGroup"
    assert obj_model1.reference_name == "myReference"

    # Populate the model from the dictionnary
    obj_model2 = ReferenceGroupModel(**obj_dict)
    assert obj_model2.class_name == "ReferenceGroup"
    assert obj_model2.id_name == "myReferenceGroup"
    assert obj_model2.reference_name == "myReference"