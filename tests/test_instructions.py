import pytest

from lammpsinputbuilder.instructions import ResetTimestepInstruction, SetTimestepInstruction, \
    VelocityCreateInstruction, DisplaceAtomsInstruction, ManualInstruction, \
    VariableStyle, VariableInstruction
from lammpsinputbuilder.types import LammpsUnitSystem, GlobalInformation
from lammpsinputbuilder.quantities import TimeQuantity, TemperatureQuantity, LengthQuantity
from lammpsinputbuilder.group import AllGroup

def test_instructions_ResetTimestep():
    instruction = ResetTimestepInstruction(instruction_name="defaultResetTimestep", new_timestep=20)
    assert instruction.get_new_timestep() == 20
    assert instruction.get_instruction_name() == "defaultResetTimestep"

    info = GlobalInformation()
    assert instruction.write_instruction(info) == "reset_timestep 20\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class_name"] == "ResetTimestepInstruction"
    assert obj_dict["new_timestep"] == 20
    assert obj_dict["id_name"] == "defaultResetTimestep"

    instruction2 = ResetTimestepInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_new_timestep() == 20
    assert instruction2.get_instruction_name() == "defaultResetTimestep"

def test_instructions_SetTimestep():
    instruction = SetTimestepInstruction(instruction_name="defaultSetTimestep", timestep=TimeQuantity(20, "fs"))
    assert instruction.get_timestep().get_magnitude() == 20
    assert instruction.get_timestep().get_units() == "fs"
    assert instruction.get_instruction_name() == "defaultSetTimestep"

    info_real = GlobalInformation()
    info_real.set_unit_style(LammpsUnitSystem.REAL)
    assert instruction.write_instruction(info_real) == "timestep 20.0\n"

    info_metal = GlobalInformation()
    info_metal.set_unit_style(LammpsUnitSystem.METAL)
    assert instruction.write_instruction(info_metal) == "timestep 0.02\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class_name"] == "SetTimestepInstruction"
    assert obj_dict["timestep"]["magnitude"] == 20
    assert obj_dict["timestep"]["units"] == "fs"
    assert obj_dict["id_name"] == "defaultSetTimestep"

    instruction2 = SetTimestepInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_timestep().get_magnitude() == 20
    assert instruction2.get_timestep().get_units() == "fs"
    assert instruction2.get_instruction_name() == "defaultSetTimestep"

def test_instruction_VelocityCreate():
    instruction = VelocityCreateInstruction(instruction_name="defaultVelocityCreate", group=AllGroup(), temp=TemperatureQuantity(300, "kelvin"), seed=12335)
    assert instruction.get_group_name() == "all"
    assert instruction.get_temp().get_magnitude() == 300
    assert instruction.get_temp().get_units() == "kelvin"
    assert instruction.get_seed() == 12335
    assert instruction.get_instruction_name() == "defaultVelocityCreate"

    info_real = GlobalInformation()
    info_real.set_unit_style(LammpsUnitSystem.REAL)
    assert instruction.write_instruction(info_real) == "velocity all create 300.0 12335 dist gaussian\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class_name"] == "VelocityCreateInstruction"
    assert obj_dict["group_name"] == "all"
    assert obj_dict["temp"]["magnitude"] == 300
    assert obj_dict["temp"]["units"] == "kelvin"
    assert obj_dict["seed"] == 12335
    assert obj_dict["id_name"] == "defaultVelocityCreate"

    instruction2 = VelocityCreateInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_group_name() == "all"
    assert instruction2.get_temp().get_magnitude() == 300
    assert instruction2.get_temp().get_units() == "kelvin"
    assert instruction2.get_seed() == 12335
    assert instruction2.get_instruction_name() == "defaultVelocityCreate"

def test_instruction_Variable():
    instruction = VariableInstruction(instruction_name="defaultVariable", variable_name="defaultVariable", style=VariableStyle.EQUAL, args="{dt}")
    assert instruction.get_variable_name() == "defaultVariable"
    assert instruction.get_variable_style() == VariableStyle.EQUAL
    assert instruction.get_args() == "{dt}"
    assert instruction.get_instruction_name() == "defaultVariable"

    info = GlobalInformation()
    assert instruction.write_instruction(info) == "variable defaultVariable equal {dt}\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class_name"] == "VariableInstruction"
    assert obj_dict["variable_name"] == "defaultVariable"
    assert obj_dict["style"] == VariableStyle.EQUAL.value
    assert obj_dict["args"] == "{dt}"
    assert obj_dict["id_name"] == "defaultVariable"

    instruction2 = VariableInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_variable_name() == "defaultVariable"
    assert instruction2.get_variable_style() == VariableStyle.EQUAL
    assert instruction2.get_args() == "{dt}"
    assert instruction2.get_instruction_name() == "defaultVariable"

def test_instruction_DisplaceAtoms():
    instruction = DisplaceAtomsInstruction(instruction_name="defaultDisplaceAtoms", group=AllGroup(), dx=LengthQuantity(1.0, "lmp_real_length"), dy=LengthQuantity(2.0, "lmp_real_length"), dz=LengthQuantity(3.0, "lmp_real_length"))
    assert instruction.get_group_name() == "all"
    displacement_vector =  instruction.get_displacement()
    assert displacement_vector[0].get_magnitude() == 1.0
    assert displacement_vector[0].get_units() == "lmp_real_length"
    assert displacement_vector[1].get_magnitude() == 2.0
    assert displacement_vector[1].get_units() == "lmp_real_length"
    assert displacement_vector[2].get_magnitude() == 3.0
    assert displacement_vector[2].get_units() == "lmp_real_length"
    assert instruction.get_instruction_name() == "defaultDisplaceAtoms"

    obj_dict = instruction.to_dict()
    assert obj_dict["class_name"] == "DisplaceAtomsInstruction"
    assert obj_dict["group_name"] == "all"
    assert obj_dict["dx"]["magnitude"] == 1.0
    assert obj_dict["dx"]["units"] == "lmp_real_length"
    assert obj_dict["dy"]["magnitude"] == 2.0
    assert obj_dict["dy"]["units"] == "lmp_real_length"
    assert obj_dict["dz"]["magnitude"] == 3.0
    assert obj_dict["dz"]["units"] == "lmp_real_length"
    assert obj_dict["id_name"] == "defaultDisplaceAtoms"

    info_real = GlobalInformation()
    info_real.set_unit_style(LammpsUnitSystem.REAL)
    assert instruction.write_instruction(info_real) == "displace_atoms all move 1.0 2.0 3.0\n"
    info_metal = GlobalInformation()
    info_metal.set_unit_style(LammpsUnitSystem.METAL)
    assert instruction.write_instruction(info_metal) == "displace_atoms all move 1.0 2.0 3.0\n"

def test_instruction_Manual():
    instruction = ManualInstruction(instruction_name="defaultManual", cmd="manual")
    assert instruction.get_instruction_name() == "defaultManual"
    assert instruction.write_instruction(GlobalInformation()) == "manual\n"
    assert instruction.get_cmd() == "manual"

    obj_dict = instruction.to_dict()
    assert obj_dict["class_name"] == "ManualInstruction"
    assert obj_dict["id_name"] == "defaultManual"
    assert obj_dict["cmd"] == "manual"

    instruction2 = ManualInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_instruction_name() == "defaultManual"
    assert instruction2.write_instruction(GlobalInformation()) == "manual\n"

def test_wrong_name():
    with pytest.raises(ValueError):
        obj = ManualInstruction(instruction_name="&&&", cmd="manual")
        del obj