import copy 

from lammpsinputbuilder.computations import * 

class ComputationLoader():
    def __init__(self) -> None:
            pass

    def dictToComputation(self, d:dict, version:int=0):
        computationTable = {}
        computationTable[SetForceCompute.__name__] = SetForceCompute()
        computationTable[LangevinCompute.__name__] = LangevinCompute()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in computationTable.keys():
            raise RuntimeError(f"Unknown Computations class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(computationTable[className])
        obj.fromDict(d, version)

        return obj