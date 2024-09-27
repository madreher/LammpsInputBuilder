from lammpsinputbuilder.instructions import ResetTimestepInstruction, SetTimestepInstruction, \
    VelocityCreateInstruction, DisplaceAtomsInstruction, ManualInstruction, \
    VariableStyle, VariableInstruction
from lammpsinputbuilder.types import LammpsUnitSystem, GlobalInformation
from lammpsinputbuilder.quantities import TimeQuantity, TemperatureQuantity, LengthQuantity
from lammpsinputbuilder.group import AllGroup

def test_instructions_ResetTimestep():
    instruction = ResetTimestepInstruction(instruction_name="defaultResetTimestep", timestep=20)
    assert instruction.get_timestep() == 20
    assert instruction.getInstructionName() == "defaultResetTimestep"

    info = GlobalInformation()
    assert instruction.write_instruction(info) == "reset_timestep 20\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class"] == "ResetTimestepInstruction"
    assert obj_dict["timestep"] == 20
    assert obj_dict["instruction_name"] == "defaultResetTimestep"

    instruction2 = ResetTimestepInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_timestep() == 20
    assert instruction2.getInstructionName() == "defaultResetTimestep"

def test_instructions_SetTimestep():
    instruction = SetTimestepInstruction(instruction_name="defaultSetTimestep", timestep=TimeQuantity(20, "fs"))
    assert instruction.get_timestep().getMagnitude() == 20
    assert instruction.get_timestep().getUnits() == "fs"
    assert instruction.getInstructionName() == "defaultSetTimestep"

    info_real = GlobalInformation()
    info_real.setUnitStyle(LammpsUnitSystem.REAL)
    assert instruction.write_instruction(info_real) == "timestep 20.0\n"

    info_metal = GlobalInformation()
    info_metal.setUnitStyle(LammpsUnitSystem.METAL)
    assert instruction.write_instruction(info_metal) == "timestep 0.02\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class"] == "SetTimestepInstruction"
    assert obj_dict["timestep"]["magnitude"] == 20
    assert obj_dict["timestep"]["units"] == "fs"
    assert obj_dict["instruction_name"] == "defaultSetTimestep"

    instruction2 = SetTimestepInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_timestep().getMagnitude() == 20
    assert instruction2.get_timestep().getUnits() == "fs"
    assert instruction2.getInstructionName() == "defaultSetTimestep"

def test_instruction_VelocityCreate():
    instruction = VelocityCreateInstruction(instruction_name="defaultVelocityCreate", group=AllGroup(), temp=TemperatureQuantity(300, "kelvin"), seed=12335)
    assert instruction.get_group_name() == "all"
    assert instruction.get_temp().getMagnitude() == 300
    assert instruction.get_temp().getUnits() == "kelvin"
    assert instruction.get_seed() == 12335
    assert instruction.getInstructionName() == "defaultVelocityCreate"

    info_real = GlobalInformation()
    info_real.setUnitStyle(LammpsUnitSystem.REAL)
    assert instruction.write_instruction(info_real) == "velocity all create 300.0 12335 dist gaussian\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class"] == "VelocityCreateInstruction"
    assert obj_dict["group_name"] == "all"
    assert obj_dict["temp"]["magnitude"] == 300
    assert obj_dict["temp"]["units"] == "kelvin"
    assert obj_dict["seed"] == 12335
    assert obj_dict["instruction_name"] == "defaultVelocityCreate"

    instruction2 = VelocityCreateInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_group_name() == "all"
    assert instruction2.get_temp().getMagnitude() == 300
    assert instruction2.get_temp().getUnits() == "kelvin"
    assert instruction2.get_seed() == 12335
    assert instruction2.getInstructionName() == "defaultVelocityCreate"

def test_instruction_Variable():
    instruction = VariableInstruction(instruction_name="defaultVariable", variable_name="defaultVariable", style=VariableStyle.EQUAL, args="{dt}")
    assert instruction.get_variable_name() == "defaultVariable"
    assert instruction.get_variable_style() == VariableStyle.EQUAL
    assert instruction.get_args() == "{dt}"
    assert instruction.getInstructionName() == "defaultVariable"

    info = GlobalInformation()
    assert instruction.write_instruction(info) == "variable defaultVariable equal {dt}\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class"] == "VariableInstruction"
    assert obj_dict["variable_name"] == "defaultVariable"
    assert obj_dict["style"] == VariableStyle.EQUAL.value
    assert obj_dict["args"] == "{dt}"
    assert obj_dict["instruction_name"] == "defaultVariable"

    instruction2 = VariableInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.get_variable_name() == "defaultVariable"
    assert instruction2.get_variable_style() == VariableStyle.EQUAL
    assert instruction2.get_args() == "{dt}"
    assert instruction2.getInstructionName() == "defaultVariable"

def test_instruction_DisplaceAtoms():
    instruction = DisplaceAtomsInstruction(instruction_name="defaultDisplaceAtoms", group=AllGroup(), dx=LengthQuantity(1.0, "lmp_real_length"), dy=LengthQuantity(2.0, "lmp_real_length"), dz=LengthQuantity(3.0, "lmp_real_length"))
    assert instruction.get_group_name() == "all"
    displacement_vector =  instruction.get_displacement()
    assert displacement_vector[0].getMagnitude() == 1.0
    assert displacement_vector[0].getUnits() == "lmp_real_length"
    assert displacement_vector[1].getMagnitude() == 2.0
    assert displacement_vector[1].getUnits() == "lmp_real_length"
    assert displacement_vector[2].getMagnitude() == 3.0
    assert displacement_vector[2].getUnits() == "lmp_real_length"
    assert instruction.getInstructionName() == "defaultDisplaceAtoms"

    info_real = GlobalInformation()
    info_real.setUnitStyle(LammpsUnitSystem.REAL)
    assert instruction.write_instruction(info_real) == "displace_atoms all move 1.0 2.0 3.0\n"
    info_metal = GlobalInformation()
    info_metal.setUnitStyle(LammpsUnitSystem.METAL)
    assert instruction.write_instruction(info_metal) == "displace_atoms all move 1.0 2.0 3.0\n"

def test_instruction_Manual():
    instruction = ManualInstruction(instruction_name="defaultManual", cmd="manual")
    assert instruction.getInstructionName() == "defaultManual"
    assert instruction.write_instruction(GlobalInformation()) == "manual\n"

    obj_dict = instruction.to_dict()
    assert obj_dict["class"] == "ManualInstruction"
    assert obj_dict["instruction_name"] == "defaultManual"
    assert obj_dict["cmd"] == "manual"

    instruction2 = ManualInstruction()
    instruction2.from_dict(obj_dict, version=0)
    assert instruction2.getInstructionName() == "defaultManual"
    assert instruction2.write_instruction(GlobalInformation()) == "manual\n"