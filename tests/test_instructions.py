from lammpsinputbuilder.instructions import *

def test_instructionsResetTimestep():
    instruction = ResetTimestepInstruction(instructionName="defaultResetTimestep", timestep=20)
    assert instruction.getTimestep() == 20
    assert instruction.getInstructionName() == "defaultResetTimestep"

    info = GlobalInformation()
    assert instruction.writeInstruction(info) == "reset_timestep 20\n"

    objDict = instruction.toDict()
    assert objDict["class"] == "ResetTimestepInstruction"
    assert objDict["timestep"] == 20
    assert objDict["instructionName"] == "defaultResetTimestep"

    instruction2 = ResetTimestepInstruction()
    instruction2.fromDict(objDict, version=0)
    assert instruction2.getTimestep() == 20
    assert instruction2.getInstructionName() == "defaultResetTimestep"

def test_instructionsSetTimestep():
    instruction = SetTimestepInstruction(instructionName="defaultSetTimestep", timestep=TimeQuantity(20, "fs"))
    assert instruction.getTimestep().getMagnitude() == 20
    assert instruction.getTimestep().getUnits() == "fs"
    assert instruction.getInstructionName() == "defaultSetTimestep"

    infoReal = GlobalInformation()
    infoReal.setUnitStyle(LammpsUnitSystem.REAL)
    assert instruction.writeInstruction(infoReal) == "timestep 20.0\n"

    infoMetal = GlobalInformation()
    infoMetal.setUnitStyle(LammpsUnitSystem.METAL)
    assert instruction.writeInstruction(infoMetal) == "timestep 0.02\n"

    objDict = instruction.toDict()
    assert objDict["class"] == "SetTimestepInstruction"
    assert objDict["timestep"]["magnitude"] == 20
    assert objDict["timestep"]["units"] == "fs"
    assert objDict["instructionName"] == "defaultSetTimestep"

    instruction2 = SetTimestepInstruction()
    instruction2.fromDict(objDict, version=0)
    assert instruction2.getTimestep().getMagnitude() == 20
    assert instruction2.getTimestep().getUnits() == "fs"
    assert instruction2.getInstructionName() == "defaultSetTimestep"

def test_instructionVelocityCreate():
    instruction = VelocityCreateInstruction(instructionName="defaultVelocityCreate", group=AllGroup(), temp=TemperatureQuantity(300, "kelvin"), seed=12335)
    assert instruction.getGroupName() == "all"
    assert instruction.getTemp().getMagnitude() == 300
    assert instruction.getTemp().getUnits() == "kelvin"
    assert instruction.getSeed() == 12335
    assert instruction.getInstructionName() == "defaultVelocityCreate"

    infoReal = GlobalInformation()
    infoReal.setUnitStyle(LammpsUnitSystem.REAL)
    assert instruction.writeInstruction(infoReal) == "velocity all create 300.0 12335 dist gaussian\n"

    objDict = instruction.toDict()
    assert objDict["class"] == "VelocityCreateInstruction"
    assert objDict["groupName"] == "all"
    assert objDict["temp"]["magnitude"] == 300
    assert objDict["temp"]["units"] == "kelvin"
    assert objDict["seed"] == 12335
    assert objDict["instructionName"] == "defaultVelocityCreate"

    instruction2 = VelocityCreateInstruction()
    instruction2.fromDict(objDict, version=0)
    assert instruction2.getGroupName() == "all"
    assert instruction2.getTemp().getMagnitude() == 300
    assert instruction2.getTemp().getUnits() == "kelvin"
    assert instruction2.getSeed() == 12335
    assert instruction2.getInstructionName() == "defaultVelocityCreate"

def test_instructionVariable():
    instruction = VariableInstruction(instructionName="defaultVariable", variableName="defaultVariable", style=VariableStyle.EQUAL, args="{dt}")
    assert instruction.getVariableName() == "defaultVariable"
    assert instruction.getVariableStyle() == VariableStyle.EQUAL
    assert instruction.getArgs() == "{dt}"
    assert instruction.getInstructionName() == "defaultVariable"

    info = GlobalInformation()
    assert instruction.writeInstruction(info) == "variable defaultVariable equal {dt}\n"

    objDict = instruction.toDict()
    assert objDict["class"] == "VariableInstruction"
    assert objDict["variableName"] == "defaultVariable"
    assert objDict["style"] == VariableStyle.EQUAL.value
    assert objDict["args"] == "{dt}"
    assert objDict["instructionName"] == "defaultVariable"

    instruction2 = VariableInstruction()
    instruction2.fromDict(objDict, version=0)
    assert instruction2.getVariableName() == "defaultVariable"
    assert instruction2.getVariableStyle() == VariableStyle.EQUAL
    assert instruction2.getArgs() == "{dt}"
    assert instruction2.getInstructionName() == "defaultVariable"

def test_DisplaceAtomsInstruction():
    instruction = DisplaceAtomsInstruction(instructionName="defaultDisplaceAtoms", group=AllGroup(), dx=LengthQuantity(1.0, "lmp_real_length"), dy=LengthQuantity(2.0, "lmp_real_length"), dz=LengthQuantity(3.0, "lmp_real_length"))
    assert instruction.getGroupName() == "all"
    displacementVector =  instruction.getDisplacement()
    assert displacementVector[0].getMagnitude() == 1.0
    assert displacementVector[0].getUnits() == "lmp_real_length"
    assert displacementVector[1].getMagnitude() == 2.0
    assert displacementVector[1].getUnits() == "lmp_real_length"
    assert displacementVector[2].getMagnitude() == 3.0
    assert displacementVector[2].getUnits() == "lmp_real_length"
    assert instruction.getInstructionName() == "defaultDisplaceAtoms"

    infoReal = GlobalInformation()
    infoReal.setUnitStyle(LammpsUnitSystem.REAL)
    assert instruction.writeInstruction(infoReal) == "displace_atoms all move 1.0 2.0 3.0\n"
    infoMetal = GlobalInformation()
    infoMetal.setUnitStyle(LammpsUnitSystem.METAL)
    assert instruction.writeInstruction(infoMetal) == "displace_atoms all move 1.0 2.0 3.0\n"