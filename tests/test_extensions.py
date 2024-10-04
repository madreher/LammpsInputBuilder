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
    assert obj.vx.get_magnitude() == 1.0
    assert obj.vx.get_units() == "angstrom/ps"
    assert obj.vy.get_magnitude() == 2.0
    assert obj.vy.get_units() == "angstrom/ps"
    assert obj.vz.get_magnitude() == 3.0
    assert obj.vz.get_units() == "angstrom/ps"

    dict_result = obj.to_dict()
    assert dict_result["group_name"] == "all"
    assert dict_result["vx"]["magnitude"] == 1.0
    assert dict_result["vx"]["units"] == "angstrom/ps"
    assert dict_result["vy"]["magnitude"] == 2.0
    assert dict_result["vy"]["units"] == "angstrom/ps"
    assert dict_result["vz"]["magnitude"] == 3.0
    assert dict_result["vz"]["units"] == "angstrom/ps"
    assert dict_result["class_name"] == "MoveExtension"

    load_back_obj = MoveExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.group == "all"
    assert load_back_obj.vx.get_magnitude() == 1.0
    assert load_back_obj.vx.get_units() == "angstrom/ps"
    assert load_back_obj.vy.get_magnitude() == 2.0
    assert load_back_obj.vy.get_units() == "angstrom/ps"
    assert load_back_obj.vz.get_magnitude() == 3.0
    assert load_back_obj.vz.get_units() == "angstrom/ps"

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
    assert obj.fx.get_magnitude() == 1.0
    assert obj.fx.get_units() == "lmp_real_force"
    assert obj.fy.get_magnitude() == 2.0
    assert obj.fy.get_units() == "lmp_real_force"
    assert obj.fz.get_magnitude() == 3.0
    assert obj.fz.get_units() == "lmp_real_force"

    dict_result = obj.to_dict()
    assert dict_result["group_name"] == "all"
    assert dict_result["fx"]["magnitude"] == 1.0
    assert dict_result["fx"]["units"] == "lmp_real_force"
    assert dict_result["fy"]["magnitude"] == 2.0
    assert dict_result["fy"]["units"] == "lmp_real_force"
    assert dict_result["fz"]["magnitude"] == 3.0
    assert dict_result["fz"]["units"] == "lmp_real_force"
    assert dict_result["class_name"] == "SetForceExtension"

    load_back_obj = SetForceExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.group == "all"
    assert load_back_obj.fx.get_magnitude() == 1.0
    assert load_back_obj.fx.get_units() == "lmp_real_force"
    assert load_back_obj.fy.get_magnitude() == 2.0
    assert load_back_obj.fy.get_units() == "lmp_real_force"
    assert load_back_obj.fz.get_magnitude() == 3.0
    assert load_back_obj.fz.get_units() == "lmp_real_force"

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
        start_temp=TemperatureQuantity(1.0, "K"), 
        end_temp=TemperatureQuantity(2.0, "K"), 
        damp=TimeQuantity(3.0, "ps"), 
        seed=122345)
    
    assert obj.group == "all"
    assert obj.start_temp.get_magnitude() == 1.0
    assert obj.start_temp.get_units() == "K"
    assert obj.end_temp.get_magnitude() == 2.0
    assert obj.end_temp.get_units() == "K"
    assert obj.damp.get_magnitude() == 3.0
    assert obj.damp.get_units() == "ps"
    assert obj.seed == 122345

    dict_result = obj.to_dict()
    assert dict_result["group_name"] == "all"
    assert dict_result["start_temp"]["magnitude"] == 1.0
    assert dict_result["start_temp"]["units"] == "K"
    assert dict_result["end_temp"]["magnitude"] == 2.0
    assert dict_result["end_temp"]["units"] == "K"
    assert dict_result["damp"]["magnitude"] == 3.0
    assert dict_result["damp"]["units"] == "ps"
    assert dict_result["seed"] == 122345
    assert dict_result["class_name"] == "LangevinExtension"

    load_back_obj = LangevinExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.group == "all"
    assert load_back_obj.start_temp.get_magnitude() == 1.0
    assert load_back_obj.start_temp.get_units() == "K"
    assert load_back_obj.end_temp.get_magnitude() == 2.0
    assert load_back_obj.end_temp.get_units() == "K"
    assert load_back_obj.damp.get_magnitude() == 3.0
    assert load_back_obj.damp.get_units() == "ps"
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
            new_timestep=10
        )
    obj = InstructionExtension(
        instruction=instr)

    dict_result = obj.to_dict()
    assert dict_result["instruction"] == instr.to_dict()
    assert dict_result["class_name"] == "InstructionExtension"

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

    assert obj.get_extension_name() == "myManualExtension"
    assert obj.do_cmd == "my_do_cmd"
    assert obj.undo_cmd == "my_undo_cmd"

    dict_result = obj.to_dict()
    assert dict_result["id_name"] == "myManualExtension"
    assert dict_result["do_cmd"] == "my_do_cmd"
    assert dict_result["undo_cmd"] == "my_undo_cmd"
    assert dict_result["class_name"] == "ManualExtension"

    load_back_obj = ManualExtension()
    load_back_obj.from_dict(dict_result, version=0)

    assert load_back_obj.get_extension_name() == "myManualExtension"
    assert load_back_obj.do_cmd == "my_do_cmd"
    assert load_back_obj.undo_cmd == "my_undo_cmd"

    assert load_back_obj.to_dict() == dict_result

def test_wrong_name():
    with pytest.raises(ValueError):
        obj = ManualExtension(
            extension_name="&&&",
            do_cmd="my_do_cmd",
            undo_cmd="my_undo_cmd"
        )
        del obj



