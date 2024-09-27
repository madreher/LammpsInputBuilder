import pytest

from lammpsinputbuilder.extensions import MoveExtension, LangevinExtension, SetForceExtension, ManualExtension, InstructionExtension
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.quantities import VelocityQuantity, LammpsUnitSystem, TemperatureQuantity, TimeQuantity, ForceQuantity
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

    dictResult = obj.to_dict()
    assert dictResult["group"] == "all"
    assert dictResult["vx"]["magnitude"] == 1.0
    assert dictResult["vx"]["units"] == "angstrom/ps"
    assert dictResult["vy"]["magnitude"] == 2.0
    assert dictResult["vy"]["units"] == "angstrom/ps"
    assert dictResult["vz"]["magnitude"] == 3.0
    assert dictResult["vz"]["units"] == "angstrom/ps"
    assert dictResult["class"] == "MoveExtension"

    loadBackObj = MoveExtension()
    loadBackObj.from_dict(dictResult, version=0)

    assert loadBackObj.group == "all"
    assert loadBackObj.vx.getMagnitude() == 1.0
    assert loadBackObj.vx.getUnits() == "angstrom/ps"
    assert loadBackObj.vy.getMagnitude() == 2.0
    assert loadBackObj.vy.getUnits() == "angstrom/ps"
    assert loadBackObj.vz.getMagnitude() == 3.0
    assert loadBackObj.vz.getUnits() == "angstrom/ps"

    assert loadBackObj.to_dict() == dictResult

    info_metal = GlobalInformation()
    info_metal.setUnitStyle(LammpsUnitSystem.METAL)
    assert obj.add_do_commands(info_metal) == "fix myMoveExtension all move linear 1.0 2.0 3.0\n"
    info_real = GlobalInformation()
    info_real.setUnitStyle(LammpsUnitSystem.REAL)
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

    dictResult = obj.to_dict()
    assert dictResult["group"] == "all"
    assert dictResult["fx"]["magnitude"] == 1.0
    assert dictResult["fx"]["units"] == "lmp_real_force"
    assert dictResult["fy"]["magnitude"] == 2.0
    assert dictResult["fy"]["units"] == "lmp_real_force"
    assert dictResult["fz"]["magnitude"] == 3.0
    assert dictResult["fz"]["units"] == "lmp_real_force"
    assert dictResult["class"] == "SetForceExtension"

    loadBackObj = SetForceExtension()
    loadBackObj.from_dict(dictResult, version=0)

    assert loadBackObj.group == "all"
    assert loadBackObj.fx.getMagnitude() == 1.0
    assert loadBackObj.fx.getUnits() == "lmp_real_force"
    assert loadBackObj.fy.getMagnitude() == 2.0
    assert loadBackObj.fy.getUnits() == "lmp_real_force"
    assert loadBackObj.fz.getMagnitude() == 3.0
    assert loadBackObj.fz.getUnits() == "lmp_real_force"

    assert loadBackObj.to_dict() == dictResult

    info_metal = GlobalInformation()
    info_metal.setUnitStyle(LammpsUnitSystem.METAL)
    assert obj.add_do_commands(info_metal) == "fix mySetForceExtension all setforce 0.04336410424180094 0.08672820848360188 0.13009231272540284\n"
    info_real = GlobalInformation()
    info_real.setUnitStyle(LammpsUnitSystem.REAL)
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

    dictResult = obj.to_dict()
    assert dictResult["group"] == "all"
    assert dictResult["startTemp"]["magnitude"] == 1.0
    assert dictResult["startTemp"]["units"] == "K"
    assert dictResult["endTemp"]["magnitude"] == 2.0
    assert dictResult["endTemp"]["units"] == "K"
    assert dictResult["damp"]["magnitude"] == 3.0
    assert dictResult["damp"]["units"] == "ps"
    assert dictResult["seed"] == 122345
    assert dictResult["class"] == "LangevinExtension"

    loadBackObj = LangevinExtension()
    loadBackObj.from_dict(dictResult, version=0)

    assert loadBackObj.group == "all"
    assert loadBackObj.startTemp.getMagnitude() == 1.0
    assert loadBackObj.startTemp.getUnits() == "K"
    assert loadBackObj.endTemp.getMagnitude() == 2.0
    assert loadBackObj.endTemp.getUnits() == "K"
    assert loadBackObj.damp.getMagnitude() == 3.0
    assert loadBackObj.damp.getUnits() == "ps"
    assert loadBackObj.seed == 122345

    assert loadBackObj.to_dict() == dictResult

    info_metal = GlobalInformation()
    info_metal.setUnitStyle(LammpsUnitSystem.METAL)
    assert obj.add_do_commands(info_metal) == "fix myLangevinExtension all langevin 1.0 2.0 3.0 122345\n"
    info_real = GlobalInformation()
    info_real.setUnitStyle(LammpsUnitSystem.REAL)
    assert obj.add_do_commands(info_real) == "fix myLangevinExtension all langevin 1.0 2.0 2999.9999999999995 122345\n"
    assert obj.add_undo_commands() == "unfix myLangevinExtension\n"

def test_InstructionExtension():
    instr = ResetTimestepInstruction(
            instruction_name="myInstruction", 
            timestep=10
        )
    obj = InstructionExtension(
        instruction=instr)

    dictResult = obj.to_dict()
    assert dictResult["instruction"] == instr.to_dict()
    assert dictResult["class"] == "InstructionExtension"

    loadBackObj = InstructionExtension()
    loadBackObj.from_dict(dictResult, version=0)

    assert loadBackObj.instruction.to_dict() == instr.to_dict()

    assert loadBackObj.to_dict() == dictResult

def test_ManualExtension():
    obj = ManualExtension(
        extension_name="myManualExtension",
        doCmd="myDoCmd",
        undoCmd="myUndoCmd"
    )

    assert obj.extension_name == "myManualExtension"
    assert obj.doCmd == "myDoCmd"
    assert obj.undoCmd == "myUndoCmd"

    dictResult = obj.to_dict()
    assert dictResult["extension_name"] == "myManualExtension"
    assert dictResult["doCmd"] == "myDoCmd"
    assert dictResult["undoCmd"] == "myUndoCmd"
    assert dictResult["class"] == "ManualExtension"

    loadBackObj = ManualExtension()
    loadBackObj.from_dict(dictResult, version=0)

    assert loadBackObj.extension_name == "myManualExtension"
    assert loadBackObj.doCmd == "myDoCmd"
    assert loadBackObj.undoCmd == "myUndoCmd"

    assert loadBackObj.to_dict() == dictResult




