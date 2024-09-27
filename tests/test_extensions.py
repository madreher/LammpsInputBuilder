import pytest

from lammpsinputbuilder.extensions import MoveExtension, LangevinExtension, \
    SetForceExtension, ManualExtension, InstructionExtension
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.quantities import VelocityQuantity, LammpsUnitSystem, \
    TemperatureQuantity, TimeQuantity, ForceQuantity
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.instructions import ResetTimestepInstruction

def test_MoveExtension():
    obj  = MoveExtension("myMoveExtension", group=AllGroup(), vx=VelocityQuantity(1.0, "angstrom/ps"), vy=VelocityQuantity(2.0, "angstrom/ps"), vz=VelocityQuantity(3.0, "angstrom/ps"))
    assert obj.group == "all"
    assert obj.vx.getMagnitude() == 1.0
    assert obj.vx.getUnits() == "angstrom/ps"
    assert obj.vy.getMagnitude() == 2.0
    assert obj.vy.getUnits() == "angstrom/ps"
    assert obj.vz.getMagnitude() == 3.0
    assert obj.vz.getUnits() == "angstrom/ps"

    dict_result = obj.to_dict()
    assert dict_result["group"] == "all"
    assert dict_result["vx"]["magnitude"] == 1.0
    assert dict_result["vx"]["units"] == "angstrom/ps"
    assert dict_result["vy"]["magnitude"] == 2.0
    assert dict_result["vy"]["units"] == "angstrom/ps"
    assert dict_result["vz"]["magnitude"] == 3.0
    assert dict_result["vz"]["units"] == "angstrom/ps"
    assert dict_result["class"] == "MoveExtension"

    load_back_obj = MoveExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.group == "all"
    assert load_back_obj.vx.getMagnitude() == 1.0
    assert load_back_obj.vx.getUnits() == "angstrom/ps"
    assert load_back_obj.vy.getMagnitude() == 2.0
    assert load_back_obj.vy.getUnits() == "angstrom/ps"
    assert load_back_obj.vz.getMagnitude() == 3.0
    assert load_back_obj.vz.getUnits() == "angstrom/ps"

    assert load_back_obj.to_dict() == dict_result

    info_metal = GlobalInformation()
    info_metal.set_unit_style(LammpsUnitSystem.METAL)
    assert obj.add_do_commands(info_metal) == "fix myMoveExtension all move linear 1.0 2.0 3.0\n"
    info_real = GlobalInformation()
    info_real.set_unit_style(LammpsUnitSystem.REAL)
    assert obj.add_do_commands(info_real) == "fix myMoveExtension all move linear 0.001 0.002 0.003\n"
    assert obj.add_undo_commands() == "unfix myMoveExtension\n"

def test_SetForceExtension():
    obj = SetForceExtension(
        "mySetForceExtension", 
        group=AllGroup(), 
        fx=ForceQuantity(1.0, "lmp_real_force"), 
        fy=ForceQuantity(2.0, "lmp_real_force"), 
        fz=ForceQuantity(3.0, "lmp_real_force"))

    assert obj.group == "all"
    assert obj.fx.getMagnitude() == 1.0
    assert obj.fx.getUnits() == "lmp_real_force"
    assert obj.fy.getMagnitude() == 2.0
    assert obj.fy.getUnits() == "lmp_real_force"
    assert obj.fz.getMagnitude() == 3.0
    assert obj.fz.getUnits() == "lmp_real_force"

    dict_result = obj.to_dict()
    assert dict_result["group"] == "all"
    assert dict_result["fx"]["magnitude"] == 1.0
    assert dict_result["fx"]["units"] == "lmp_real_force"
    assert dict_result["fy"]["magnitude"] == 2.0
    assert dict_result["fy"]["units"] == "lmp_real_force"
    assert dict_result["fz"]["magnitude"] == 3.0
    assert dict_result["fz"]["units"] == "lmp_real_force"
    assert dict_result["class"] == "SetForceExtension"

    load_back_obj = SetForceExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.group == "all"
    assert load_back_obj.fx.getMagnitude() == 1.0
    assert load_back_obj.fx.getUnits() == "lmp_real_force"
    assert load_back_obj.fy.getMagnitude() == 2.0
    assert load_back_obj.fy.getUnits() == "lmp_real_force"
    assert load_back_obj.fz.getMagnitude() == 3.0
    assert load_back_obj.fz.getUnits() == "lmp_real_force"

    assert load_back_obj.to_dict() == dict_result

    info_metal = GlobalInformation()
    info_metal.set_unit_style(LammpsUnitSystem.METAL)
    assert obj.add_do_commands(info_metal) == "fix mySetForceExtension all setforce 0.04336410424180094 0.08672820848360188 0.13009231272540284\n"
    info_real = GlobalInformation()
    info_real.set_unit_style(LammpsUnitSystem.REAL)
    assert obj.add_do_commands(info_real) == "fix mySetForceExtension all setforce 1.0 2.0 3.0\n"
    assert obj.add_undo_commands() == "unfix mySetForceExtension\n"

def test_LangevinExtension():
    obj = LangevinExtension(
        "myLangevinExtension", 
        group=AllGroup(), 
        startTemp=TemperatureQuantity(1.0, "K"), 
        endTemp=TemperatureQuantity(2.0, "K"), 
        damp=TimeQuantity(3.0, "ps"), 
        seed=122345)
    
    assert obj.group == "all"
    assert obj.startTemp.getMagnitude() == 1.0
    assert obj.startTemp.getUnits() == "K"
    assert obj.endTemp.getMagnitude() == 2.0
    assert obj.endTemp.getUnits() == "K"
    assert obj.damp.getMagnitude() == 3.0
    assert obj.damp.getUnits() == "ps"
    assert obj.seed == 122345

    dict_result = obj.to_dict()
    assert dict_result["group"] == "all"
    assert dict_result["startTemp"]["magnitude"] == 1.0
    assert dict_result["startTemp"]["units"] == "K"
    assert dict_result["endTemp"]["magnitude"] == 2.0
    assert dict_result["endTemp"]["units"] == "K"
    assert dict_result["damp"]["magnitude"] == 3.0
    assert dict_result["damp"]["units"] == "ps"
    assert dict_result["seed"] == 122345
    assert dict_result["class"] == "LangevinExtension"

    load_back_obj = LangevinExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.group == "all"
    assert load_back_obj.startTemp.getMagnitude() == 1.0
    assert load_back_obj.startTemp.getUnits() == "K"
    assert load_back_obj.endTemp.getMagnitude() == 2.0
    assert load_back_obj.endTemp.getUnits() == "K"
    assert load_back_obj.damp.getMagnitude() == 3.0
    assert load_back_obj.damp.getUnits() == "ps"
    assert load_back_obj.seed == 122345

    assert load_back_obj.to_dict() == dict_result

    info_metal = GlobalInformation()
    info_metal.set_unit_style(LammpsUnitSystem.METAL)
    assert obj.add_do_commands(info_metal) == "fix myLangevinExtension all langevin 1.0 2.0 3.0 122345\n"
    info_real = GlobalInformation()
    info_real.set_unit_style(LammpsUnitSystem.REAL)
    assert obj.add_do_commands(info_real) == "fix myLangevinExtension all langevin 1.0 2.0 2999.9999999999995 122345\n"
    assert obj.add_undo_commands() == "unfix myLangevinExtension\n"

def test_InstructionExtension():
    instr = ResetTimestepInstruction(
            instruction_name="myInstruction", 
            timestep=10
        )
    obj = InstructionExtension(
        instruction=instr)

    dict_result = obj.to_dict()
    assert dict_result["instruction"] == instr.to_dict()
    assert dict_result["class"] == "InstructionExtension"

    load_back_obj = InstructionExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.instruction.to_dict() == instr.to_dict()

    assert load_back_obj.to_dict() == dict_result

def test_ManualExtension():
    obj = ManualExtension(
        extension_name="myManualExtension",
        do_cmd="my_do_cmd",
        undo_cmd="my_undo_cmd"
    )

    assert obj.extension_name == "myManualExtension"
    assert obj.do_cmd == "my_do_cmd"
    assert obj.undo_cmd == "my_undo_cmd"

    dict_result = obj.to_dict()
    assert dict_result["extension_name"] == "myManualExtension"
    assert dict_result["do_cmd"] == "my_do_cmd"
    assert dict_result["undo_cmd"] == "my_undo_cmd"
    assert dict_result["class"] == "ManualExtension"

    load_back_obj = ManualExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.extension_name == "myManualExtension"
    assert load_back_obj.do_cmd == "my_do_cmd"
    assert load_back_obj.undo_cmd == "my_undo_cmd"

    assert load_back_obj.to_dict() == dict_result




