"""Module faciliating the instanciation of Instruction classes."""

import copy

from lammpsinputbuilder.instructions import ResetTimestepInstruction, \
    SetTimestepInstruction, VelocityCreateInstruction, \
    DisplaceAtomsInstruction, ManualInstruction, VariableInstruction


class InstructionLoader():
    def __init__(self) -> None:
        pass

    def dict_to_instruction(self, d: dict, version: int = 0):
        instruction_table = {}
        instruction_table[ResetTimestepInstruction.__name__] = ResetTimestepInstruction(
        )
        instruction_table[SetTimestepInstruction.__name__] = SetTimestepInstruction()
        instruction_table[VelocityCreateInstruction.__name__] = VelocityCreateInstruction(
        )
        instruction_table[DisplaceAtomsInstruction.__name__] = DisplaceAtomsInstruction(
        )
        instruction_table[ManualInstruction.__name__] = ManualInstruction()
        instruction_table[VariableInstruction.__name__] = VariableInstruction()

        if "class_name" not in d:
            raise RuntimeError(f"Missing 'class_name' key in {d}.")
        class_name = d["class_name"]
        if class_name not in instruction_table:
            raise RuntimeError(f"Unknown Instruction class {class_name}.")
        # Create a copy of the base object, and we will update the settings of
        # the object from the dictionary
        obj = copy.deepcopy(instruction_table[class_name])
        obj.from_dict(d, version)

        return obj
