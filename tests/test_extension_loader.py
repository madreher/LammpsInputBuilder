import pytest

from lammpsinputbuilder.loader.extension_loader import ExtensionLoader
from lammpsinputbuilder.extensions import LangevinExtension, SetForceExtension, \
    MoveExtension, InstructionExtension, ManualExtension
from lammpsinputbuilder.instructions import ResetTimestepInstruction
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity, ForceQuantity, \
    VelocityQuantity

def test_load_langevin_extension():

    obj = LangevinExtension(
        "myLangevinExtension", 
        group=AllGroup(),
        start_temp=TemperatureQuantity(1.0, "K"),
        end_temp=TemperatureQuantity(2.0, "K"),
        damp=TimeQuantity(3.0, "ps"),
        seed=122345)

    obj_dict = obj.to_dict()
    loader = ExtensionLoader()
    obj2 = loader.dict_to_extension(obj_dict, 0)
    assert obj2.group == "all"
    assert obj2.start_temp.get_magnitude() == 1.0
    assert obj2.start_temp.get_units() == "K"
    assert obj2.end_temp.get_magnitude() == 2.0
    assert obj2.end_temp.get_units() == "K"
    assert obj2.damp.get_magnitude() == 3.0
    assert obj2.damp.get_units() == "ps"
    assert obj2.seed == 122345

def test_load_set_force_extension():

    obj = SetForceExtension(
        "mySetForceExtension", 
        group=AllGroup(),
        fx=ForceQuantity(1.0, "lmp_real_force"),
        fy=ForceQuantity(2.0, "lmp_real_force"),
        fz=ForceQuantity(3.0, "lmp_real_force"))

    obj_dict = obj.to_dict()
    loader = ExtensionLoader()
    obj2 = loader.dict_to_extension(obj_dict, 0)
    assert obj2.group == "all"
    assert obj2.fx.get_magnitude() == 1.0
    assert obj2.fx.get_units() == "lmp_real_force"
    assert obj2.fy.get_magnitude() == 2.0
    assert obj2.fy.get_units() == "lmp_real_force"
    assert obj2.fz.get_magnitude() == 3.0
    assert obj2.fz.get_units() == "lmp_real_force"

def test_load_move_extension():

    obj = MoveExtension(
        "myMoveExtension", 
        group=AllGroup(),
        vx=VelocityQuantity(1.0, "lmp_real_velocity"),
        vy=VelocityQuantity(2.0, "lmp_real_velocity"),
        vz=VelocityQuantity(3.0, "lmp_real_velocity"))

    obj_dict = obj.to_dict()
    loader = ExtensionLoader()
    obj2 = loader.dict_to_extension(obj_dict, 0)
    assert obj2.group == "all"
    assert obj2.vx.get_magnitude() == 1.0
    assert obj2.vx.get_units() == "lmp_real_velocity"
    assert obj2.vy.get_magnitude() == 2.0
    assert obj2.vy.get_units() == "lmp_real_velocity"
    assert obj2.vz.get_magnitude() == 3.0
    assert obj2.vz.get_units() == "lmp_real_velocity"

def test_load_instruction_extension():
    instr = ResetTimestepInstruction(
            instruction_name="myInstruction", 
            new_timestep=10
        )
    obj = InstructionExtension(
        instruction=instr)

    obj_dict = obj.to_dict()
    loader = ExtensionLoader()
    obj2 = loader.dict_to_extension(obj_dict, 0)
    assert obj2.instruction.get_new_timestep() == 10


def test_load_manual_extension():
    obj = ManualExtension(
        extension_name="myManualExtension",
        do_cmd="my_do_cmd",
        undo_cmd="my_undo_cmd"
    )

    obj_dict = obj.to_dict()
    loader = ExtensionLoader()
    obj2 = loader.dict_to_extension(obj_dict, 0)
    assert obj2.get_extension_name() == "myManualExtension"
    assert obj2.do_cmd == "my_do_cmd"
    assert obj2.undo_cmd == "my_undo_cmd"

def test_no_class():
    obj = ManualExtension()
    obj_dict = obj.to_dict()
    del obj_dict["class_name"]

    with pytest.raises(RuntimeError):
        loader = ExtensionLoader()
        obj2 = loader.dict_to_extension(obj_dict, 0)
        del obj2 

def test_unknown_class():
    obj = ManualExtension()
    obj_dict = obj.to_dict()
    obj_dict["class_name"] = "unknown"

    with pytest.raises(RuntimeError):
        loader = ExtensionLoader()
        obj2 = loader.dict_to_extension(obj_dict, 0)
        del obj2
