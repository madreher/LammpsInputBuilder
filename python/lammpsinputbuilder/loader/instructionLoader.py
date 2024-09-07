import copy 

from lammpsinputbuilder.instructions import * 

class InstructionLoader():
    def __init__(self) -> None:
            pass

    def dictToInstruction(self, d:dict, version:int=0):
        instructionTable = {}
        instructionTable[ResetTimestepInstruction.__name__] = ResetTimestepInstruction()
        instructionTable[SetTimestepInstruction.__name__] = SetTimestepInstruction()
        instructionTable[VelocityCreateInstruction.__name__] = VelocityCreateInstruction()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in instructionTable.keys():
            raise RuntimeError(f"Unknown Instruction class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(instructionTable[className])
        obj.fromDict(d, version)

        return obj