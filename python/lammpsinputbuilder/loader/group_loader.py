"""Module faciliating the instanciation of Group classes."""

import copy

from lammpsinputbuilder.group import AllGroup, \
    EmptyGroup, OperationGroup, IndicesGroup, \
    ReferenceGroup, ManualGroup


class GroupLoader:
    def __init__(self) -> None:
        pass

    def dict_to_group(self, d: dict, version: int = 0):
        groupe_table = {}
        groupe_table[AllGroup.__name__] = AllGroup()
        groupe_table[EmptyGroup.__name__] = EmptyGroup()
        groupe_table[OperationGroup.__name__] = OperationGroup()
        groupe_table[IndicesGroup.__name__] = IndicesGroup()
        groupe_table[ReferenceGroup.__name__] = ReferenceGroup()
        groupe_table[ManualGroup.__name__] = ManualGroup()

        if "class_name" not in d:
            raise RuntimeError(f"Missing 'class_name' key in {d}.")
        class_name = d["class_name"]
        if class_name not in groupe_table:
            raise RuntimeError(f"Unknown Group class {class_name}.")
        # Create a copy of the base object, and we will update the settings
        # of the object from the dictionary
        obj = copy.deepcopy(groupe_table[class_name])
        obj.from_dict(d, version)

        return obj
