import json 

from lammpsinputbuilder.instructions import ResetTimestepInstruction, SetTimestepInstruction, \
    VelocityCreateInstruction, DisplaceAtomsInstruction, ManualInstruction, VariableInstruction, \
    VariableStyle

from lammpsinputbuilder.model.instruction_model import ResetTimestepInstructionModel, \
    SetTimestepInstructionModel, VelocityCreateInstructionModel, DisplaceAtomsInstructionModel, \
    ManualInstructionModel, VariableInstructionModel
from lammpsinputbuilder.quantities import TimeQuantity, TemperatureQuantity, LengthQuantity
from lammpsinputbuilder.group import AllGroup

def test_reset_timestep_instruction_model():
    obj = ResetTimestepInstruction(instruction_name="defaultResetTimestep", new_timestep=20)

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = ResetTimestepInstructionModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "ResetTimestepInstruction"
    assert obj_model1.id_name == "defaultResetTimestep"
    assert obj_model1.new_timestep == 20

    # Populate the model from the dictionnary
    obj_model2 = ResetTimestepInstructionModel(**obj_dict)
    assert obj_model2.class_name == "ResetTimestepInstruction"
    assert obj_model2.id_name == "defaultResetTimestep"
    assert obj_model2.new_timestep == 20

def test_set_timestep_instruction_model():
    obj = SetTimestepInstruction(instruction_name="defaultSetTimestep", timestep=TimeQuantity(20, "fs"))

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = SetTimestepInstructionModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "SetTimestepInstruction"
    assert obj_model1.id_name == "defaultSetTimestep"
    assert obj_model1.timestep.class_name == "TimeQuantity"
    assert obj_model1.timestep.magnitude == 20
    assert obj_model1.timestep.units == "fs"

    # Populate the model from the dictionnary
    obj_model2 = SetTimestepInstructionModel(**obj_dict)
    assert obj_model2.class_name == "SetTimestepInstruction"
    assert obj_model2.id_name == "defaultSetTimestep"
    assert obj_model2.timestep.class_name == "TimeQuantity"
    assert obj_model2.timestep.magnitude == 20
    assert obj_model2.timestep.units == "fs"

def test_velocity_create_instruction_model():
    obj = VelocityCreateInstruction(
        instruction_name="defaultVelocityCreate", 
        group=AllGroup(), 
        temp=TemperatureQuantity(300, "kelvin"), 
        seed=12335)

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = VelocityCreateInstructionModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "VelocityCreateInstruction"
    assert obj_model1.id_name == "defaultVelocityCreate"
    assert obj_model1.group_name == "all"
    assert obj_model1.temp.class_name == "TemperatureQuantity"
    assert obj_model1.temp.magnitude == 300
    assert obj_model1.temp.units == "kelvin"
    assert obj_model1.seed == 12335

    # Populate the model from the dictionnary
    obj_model2 = VelocityCreateInstructionModel(**obj_dict)
    assert obj_model2.class_name == "VelocityCreateInstruction"
    assert obj_model2.id_name == "defaultVelocityCreate"
    assert obj_model2.group_name == "all"
    assert obj_model2.temp.class_name == "TemperatureQuantity"
    assert obj_model2.temp.magnitude == 300
    assert obj_model2.temp.units == "kelvin"

def test_variable_instruction_model():
    obj = VariableInstruction(
        instruction_name="defaultVariable",
        variable_name="defaultVariable",
        style=VariableStyle.EQUAL,
        args="{dt}")
    
    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = VariableInstructionModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "VariableInstruction"
    assert obj_model1.id_name == "defaultVariable"
    assert obj_model1.variable_name == "defaultVariable"
    assert obj_model1.style == VariableStyle.EQUAL
    assert obj_model1.args == "{dt}"

    # Populate the model from the dictionnary
    obj_model2 = VariableInstructionModel(**obj_dict)
    assert obj_model2.class_name == "VariableInstruction"
    assert obj_model2.id_name == "defaultVariable"
    assert obj_model2.variable_name == "defaultVariable"
    assert obj_model2.style == VariableStyle.EQUAL
    assert obj_model2.args == "{dt}"

def test_displace_atoms_instruction_model():
    obj = DisplaceAtomsInstruction(
        instruction_name="defaultDisplaceAtoms",
        group=AllGroup(),
        dx=LengthQuantity(1.0, "lmp_real_length"),
        dy=LengthQuantity(2.0, "lmp_real_length"),
        dz=LengthQuantity(3.0, "lmp_real_length"))

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = DisplaceAtomsInstructionModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "DisplaceAtomsInstruction"
    assert obj_model1.id_name == "defaultDisplaceAtoms"
    assert obj_model1.group_name == "all"
    assert obj_model1.dx.class_name == "LengthQuantity"
    assert obj_model1.dx.magnitude == 1.0
    assert obj_model1.dx.units == "lmp_real_length"
    assert obj_model1.dy.class_name == "LengthQuantity"
    assert obj_model1.dy.magnitude == 2.0
    assert obj_model1.dy.units == "lmp_real_length"
    assert obj_model1.dz.class_name == "LengthQuantity"
    assert obj_model1.dz.magnitude == 3.0
    assert obj_model1.dz.units == "lmp_real_length"

    # Populate the model from the dictionnary
    obj_model2 = DisplaceAtomsInstructionModel(**obj_dict)
    assert obj_model2.class_name == "DisplaceAtomsInstruction"
    assert obj_model2.id_name == "defaultDisplaceAtoms"
    assert obj_model2.group_name == "all"
    assert obj_model2.dx.class_name == "LengthQuantity"
    assert obj_model2.dx.magnitude == 1.0
    assert obj_model2.dx.units == "lmp_real_length"
    assert obj_model2.dy.class_name == "LengthQuantity"
    assert obj_model2.dy.magnitude == 2.0
    assert obj_model2.dy.units == "lmp_real_length"
    assert obj_model2.dz.class_name == "LengthQuantity"
    assert obj_model2.dz.magnitude == 3.0
    assert obj_model2.dz.units == "lmp_real_length"

def test_manual_instruction_model():
    obj = ManualInstruction(instruction_name="defaultManual", cmd="manual")

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = ManualInstructionModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "ManualInstruction"
    assert obj_model1.id_name == "defaultManual"
    assert obj_model1.cmd == "manual"

    # Populate the model from the dictionnary
    obj_model2 = ManualInstructionModel(**obj_dict)
    assert obj_model2.class_name == "ManualInstruction"
    assert obj_model2.id_name == "defaultManual"
    assert obj_model2.cmd == "manual"