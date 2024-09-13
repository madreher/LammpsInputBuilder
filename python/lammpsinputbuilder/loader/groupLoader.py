import copy 

from lammpsinputbuilder.group import * 

class GroupLoader:
    def __init__(self) -> None:
        pass

    def dictToGroup(self, d:dict, version:int=0):
        groupTable = {}
        groupTable[AllGroup.__name__] = AllGroup()
        groupTable[EmptyGroup.__name__] = EmptyGroup()
        groupTable[OperationGroup.__name__] = OperationGroup()
        groupTable[IndicesGroup.__name__] = IndicesGroup()
        groupTable[ReferenceGroup.__name__] = ReferenceGroup()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in groupTable.keys():
            raise RuntimeError(f"Unknown Group class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(groupTable[className])
        obj.fromDict(d, version)

        return obj