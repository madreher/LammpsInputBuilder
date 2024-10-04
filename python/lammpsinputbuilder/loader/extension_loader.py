"""Module faciliating the instanciation of Extension classes."""

import copy
from lammpsinputbuilder.extensions import \
    SetForceExtension, LangevinExtension, \
    MoveExtension, ManualExtension, \
    InstructionExtension


class ExtensionLoader():
    def __init__(self) -> None:
        pass

    def dict_to_extension(self, d: dict, version: int = 0):
        extension_table = {}
        extension_table[SetForceExtension.__name__] = SetForceExtension()
        extension_table[LangevinExtension.__name__] = LangevinExtension()
        extension_table[MoveExtension.__name__] = MoveExtension()
        extension_table[ManualExtension.__name__] = ManualExtension()
        extension_table[InstructionExtension.__name__] = InstructionExtension()

        if "class_name" not in d:
            raise RuntimeError(f"Missing 'class_name' key in {d}.")
        class_name = d["class_name"]
        if class_name not in extension_table:
            raise RuntimeError(f"Unknown Extension class {class_name}.")
        # Create a copy of the base object, and we will update the settings
        # of the object from the dictionary
        obj = copy.deepcopy(extension_table[class_name])
        obj.from_dict(d, version)

        return obj
