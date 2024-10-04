import pytest

from lammpsinputbuilder.loader.instruction_loader import InstructionLoader
from lammpsinputbuilder.instructions import ResetTimestepInstruction, SetTimestepInstruction, \
    VelocityCreateInstruction, VariableInstruction, VariableStyle, DisplaceAtomsInstruction, \
    ManualInstruction
from lammpsinputbuilder.quantities import TimeQuantity, TemperatureQuantity, LengthQuantity
from lammpsinputbuilder.group import AllGroup

def test_load_reset_timestep_instruction():
    obj = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    obj_dict = obj.to_dict()
    loader = InstructionLoader()
    obj2 = loader.dict_to_instruction(obj_dict, 0)
    assert obj2.get_instruction_name() == "myInstruction"
    assert obj2.get_new_timestep() == 10

def test_load_set_timestep_instruction():
    obj = SetTimestepInstruction(
        instruction_name="myInstruction",
        timestep=TimeQuantity(20, "fs")
    )
    obj_dict = obj.to_dict()
    loader = InstructionLoader()
    obj2 = loader.dict_to_instruction(obj_dict, 0)
    assert obj2.get_instruction_name() == "myInstruction"
    assert obj2.get_timestep().get_magnitude() == 20
    assert obj2.get_timestep().get_units() == "fs"

def test_load_velocity_create_instruction():
    obj = VelocityCreateInstruction(instruction_name="defaultVelocityCreate",
            group=AllGroup(),
            temp=TemperatureQuantity(300, "kelvin"),
            seed=12335)
    obj_dict = obj.to_dict()
    loader = InstructionLoader()
    obj2 = loader.dict_to_instruction(obj_dict, 0)
    assert obj2.get_instruction_name() == "defaultVelocityCreate"
    assert obj2.get_group_name() == "all"
    assert obj2.get_temp().get_magnitude() == 300
    assert obj2.get_temp().get_units() == "kelvin"
    assert obj2.get_seed() == 12335

def test_load_variable_instruction():
    obj = VariableInstruction(
        instruction_name="defaultVariable",
        variable_name="defaultVariable",
        style=VariableStyle.EQUAL, args="{dt}"
    )
    obj_dict = obj.to_dict()
    loader = InstructionLoader()
    obj2 = loader.dict_to_instruction(obj_dict, 0)
    assert obj2.get_instruction_name() == "defaultVariable"
    assert obj2.get_variable_name() == "defaultVariable"
    assert obj2.get_variable_style() == VariableStyle.EQUAL
    assert obj2.get_args() == "{dt}"

def test_load_displace_atoms_instruction():
    obj = DisplaceAtomsInstruction(
        instruction_name="defaultDisplaceAtoms",
        group=AllGroup(),
        dx=LengthQuantity(1.0, "lmp_real_length"),
        dy=LengthQuantity(2.0, "lmp_real_length"),
        dz=LengthQuantity(3.0, "lmp_real_length"))

    obj_dict = obj.to_dict()
    loader = InstructionLoader()
    obj2 = loader.dict_to_instruction(obj_dict, 0)
    assert obj2.get_instruction_name() == "defaultDisplaceAtoms"
    assert obj2.get_group_name() == "all"
    assert obj2.get_displacement()[0].get_magnitude() == 1.0
    assert obj2.get_displacement()[0].get_units() == "lmp_real_length"
    assert obj2.get_displacement()[1].get_magnitude() == 2.0
    assert obj2.get_displacement()[1].get_units() == "lmp_real_length"
    assert obj2.get_displacement()[2].get_magnitude() == 3.0
    assert obj2.get_displacement()[2].get_units() == "lmp_real_length"

def test_load_manual_instruction():
    obj = ManualInstruction(instruction_name="defaultManual", cmd="manual")

    obj_dict = obj.to_dict()
    loader = InstructionLoader()
    obj2 = loader.dict_to_instruction(obj_dict, 0)

    assert obj2.get_instruction_name() == "defaultManual"
    assert obj2.get_cmd() == "manual"

def test_load_no_class_instruction():
    obj = ManualInstruction(instruction_name="defaultManual", cmd="manual")

    obj_dict = obj.to_dict()
    del obj_dict["class_name"]

    with pytest.raises(RuntimeError):
        loader = InstructionLoader()
        obj2 = loader.dict_to_instruction(obj_dict, 0)
        del obj2

def test_load_unknown_class_instruction():
    obj = ManualInstruction(instruction_name="defaultManual", cmd="manual")

    obj_dict = obj.to_dict()
    obj_dict["class_name"] = "unknown"

    with pytest.raises(RuntimeError):
        loader = InstructionLoader()
        obj2 = loader.dict_to_instruction(obj_dict, 0)
        del obj2
    