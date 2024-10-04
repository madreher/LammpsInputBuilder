import json
from lammpsinputbuilder.extensions import LangevinExtension, MoveExtension, SetForceExtension, \
    InstructionExtension, ManualExtension
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity, \
    VelocityQuantity, ForceQuantity
from lammpsinputbuilder.instructions import ResetTimestepInstruction
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.model.extension_model import LangevinExtensionModel, \
    MoveExtensionModel, SetForceExtensionModel, InstructionExtensionModel, ManualExtensionModel

def test_move_extension_model():
    obj  = MoveExtension(
        "myMoveExtension", 
        group=AllGroup(), 
        vx=VelocityQuantity(1.0, "angstrom/ps"), 
        vy=VelocityQuantity(2.0, "angstrom/ps"), 
        vz=VelocityQuantity(3.0, "angstrom/ps"))
    
    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = MoveExtensionModel.model_validate_json(obj_dict_str)

    assert obj_model1.group_name == "all"
    assert obj_model1.vx.class_name == "VelocityQuantity"
    assert obj_model1.vx.magnitude == 1.0
    assert obj_model1.vx.units == "angstrom/ps"
    assert obj_model1.vy.class_name == "VelocityQuantity"
    assert obj_model1.vy.magnitude == 2.0
    assert obj_model1.vy.units == "angstrom/ps"
    assert obj_model1.vz.class_name == "VelocityQuantity"
    assert obj_model1.vz.magnitude == 3.0
    assert obj_model1.vz.units == "angstrom/ps"

    # Populate the model from the dictionnary
    obj_model2 = MoveExtensionModel(**obj_dict)
    assert obj_model2.group_name == "all"
    assert obj_model2.vx.class_name == "VelocityQuantity"
    assert obj_model2.vx.magnitude == 1.0
    assert obj_model2.vx.units == "angstrom/ps"
    assert obj_model2.vy.class_name == "VelocityQuantity"
    assert obj_model2.vy.magnitude == 2.0
    assert obj_model2.vy.units == "angstrom/ps"
    assert obj_model2.vz.class_name == "VelocityQuantity"
    assert obj_model2.vz.magnitude == 3.0
    assert obj_model2.vz.units == "angstrom/ps"

def test_setforce_extension_model():
    obj = SetForceExtension(
        "mySetForceExtension", 
        group=AllGroup(),
        fx=ForceQuantity(1.0, "lmp_real_force"),
        fy=ForceQuantity(2.0, "lmp_real_force"),
        fz=ForceQuantity(3.0, "lmp_real_force"))

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = SetForceExtensionModel.model_validate_json(obj_dict_str)

    assert obj_model1.class_name == "SetForceExtension"
    assert obj_model1.id_name == "mySetForceExtension"
    assert obj_model1.group_name == "all"
    assert obj_model1.fx.class_name == "ForceQuantity"
    assert obj_model1.fx.magnitude == 1.0
    assert obj_model1.fx.units == "lmp_real_force"
    assert obj_model1.fy.class_name == "ForceQuantity"
    assert obj_model1.fy.magnitude == 2.0
    assert obj_model1.fy.units == "lmp_real_force"
    assert obj_model1.fz.class_name == "ForceQuantity"
    assert obj_model1.fz.magnitude == 3.0
    assert obj_model1.fz.units == "lmp_real_force"

    # Populate the model from the dictionnary
    obj_model2 = SetForceExtensionModel(**obj_dict)
    assert obj_model2.class_name == "SetForceExtension"
    assert obj_model2.id_name == "mySetForceExtension"
    assert obj_model2.group_name == "all"
    assert obj_model2.fx.class_name == "ForceQuantity"
    assert obj_model2.fx.magnitude == 1.0
    assert obj_model2.fx.units == "lmp_real_force"
    assert obj_model2.fy.class_name == "ForceQuantity"
    assert obj_model2.fy.magnitude == 2.0
    assert obj_model2.fy.units == "lmp_real_force"
    assert obj_model2.fz.class_name == "ForceQuantity"
    assert obj_model2.fz.magnitude == 3.0
    assert obj_model2.fz.units == "lmp_real_force"

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

    assert obj_model1.class_name == "LangevinExtension"
    assert obj_model1.id_name == "myLangevinExtension"
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
    assert obj_model2.class_name == "LangevinExtension"
    assert obj_model2.id_name == "myLangevinExtension"
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

def test_instruction_extension_model():
    instr = ResetTimestepInstruction(
            instruction_name="myInstruction", 
            new_timestep=10
        )
    obj = InstructionExtension(
        instruction=instr)

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = InstructionExtensionModel.model_validate_json(obj_dict_str)

    assert obj_model1.class_name == "InstructionExtension"
    assert obj_model1.id_name == "myInstruction"
    assert obj_model1.instruction.class_name == "ResetTimestepInstruction"
    assert obj_model1.instruction.new_timestep == 10


    # Populate the model from the dictionnary
    obj_model2 = InstructionExtensionModel(**obj_dict)
    assert obj_model2.class_name == "InstructionExtension"
    assert obj_model2.id_name == "myInstruction"
    assert obj_model2.instruction.class_name == "ResetTimestepInstruction"
    assert obj_model2.instruction.new_timestep == 10

def test_manual_extension_model():
    obj = ManualExtension(
        extension_name="myManualExtension",
        do_cmd="my_do_cmd",
        undo_cmd="my_undo_cmd"
    )
    
    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = ManualExtensionModel.model_validate_json(obj_dict_str)

    assert obj_model1.class_name == "ManualExtension"
    assert obj_model1.id_name == "myManualExtension"
    assert obj_model1.do_cmd == "my_do_cmd"
    assert obj_model1.undo_cmd == "my_undo_cmd"

    # Populate the model from the dictionnary
    obj_model2 = ManualExtensionModel(**obj_dict)
    assert obj_model2.class_name == "ManualExtension"
    assert obj_model2.id_name == "myManualExtension"
    assert obj_model2.do_cmd == "my_do_cmd"
    assert obj_model2.undo_cmd == "my_undo_cmd"