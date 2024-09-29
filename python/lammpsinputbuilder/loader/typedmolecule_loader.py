"""Module faciliating the instanciation of TypedMolecularSystem classes."""

import copy

from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem


class TypedMolecularSystemLoader():
    def __init__(self) -> None:
        pass

    def dict_to_typed_molecular_system(self, d: dict, version: int = 0):
        molecule_table = {}
        molecule_table[ReaxTypedMolecularSystem.__name__] = ReaxTypedMolecularSystem()

        if "class" not in d:
            raise RuntimeError(f"Missing 'class' key in {d}.")
        class_name = d["class"]
        if class_name not in molecule_table:
            raise RuntimeError(
                f"Unknown TypedMolecularSystem class {class_name}.")
        # Create a copy of the base object, and we will update the settings of
        # the object from the dictionary
        obj = copy.deepcopy(molecule_table[class_name])
        obj.from_dict(d, version)

        return obj