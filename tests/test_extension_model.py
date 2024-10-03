import json
from lammpsinputbuilder.extensions import LangevinExtension
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.model.extension_model import LangevinExtensionModel

def test_langevin_extension_model():
    obj = LangevinExtension(
        "myLangevinExtension", 
        group=AllGroup(),
        start_temp=TemperatureQuantity(1.0, "K"),
        end_temp=TemperatureQuantity(2.0, "K"),
        damp=TimeQuantity(3.0, "ps"),
        seed=122345)

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = LangevinExtensionModel.model_validate_json(obj_dict_str)

    assert obj_model1.group_name == "all"
    assert obj_model1.start_temp.class_name == "TemperatureQuantity"
    assert obj_model1.start_temp.magnitude == 1.0
    assert obj_model1.start_temp.units == "K"
    assert obj_model1.end_temp.class_name == "TemperatureQuantity"
    assert obj_model1.end_temp.magnitude == 2.0
    assert obj_model1.end_temp.units == "K"
    assert obj_model1.damp.class_name == "TimeQuantity"
    assert obj_model1.damp.magnitude == 3.0
    assert obj_model1.damp.units == "ps"
    assert obj_model1.seed == 122345

    # Populate the model from the dictionnary
    obj_model2 = LangevinExtensionModel(**obj_dict)
    assert obj_model2.group_name == "all"
    assert obj_model2.start_temp.class_name == "TemperatureQuantity"
    assert obj_model2.start_temp.magnitude == 1.0
    assert obj_model2.start_temp.units == "K"
    assert obj_model2.end_temp.class_name == "TemperatureQuantity"
    assert obj_model2.end_temp.magnitude == 2.0
    assert obj_model2.end_temp.units == "K"
    assert obj_model2.damp.class_name == "TimeQuantity"
    assert obj_model2.damp.magnitude == 3.0
    assert obj_model2.damp.units == "ps"
    assert obj_model2.seed == 122345
