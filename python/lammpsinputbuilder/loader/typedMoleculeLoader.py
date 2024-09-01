import copy 

from lammpsinputbuilder.typedMolecule import * 

class TypedMoleculeLoader():
    def __init__(self) -> None:
            pass

    def dictToTypedMolecule(self, d:dict, version:int=0):
        moleculeTable = {}
        moleculeTable[ReaxTypedMolecule.__name__] = ReaxTypedMolecule()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in moleculeTable.keys():
            raise RuntimeError(f"Unknown TypedMolecule class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(moleculeTable[className])
        obj.fromDict(d, version)

        return obj