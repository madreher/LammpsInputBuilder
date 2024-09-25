import copy 

from lammpsinputbuilder.extensions import * 

class ExtensionLoader():
    def __init__(self) -> None:
            pass

    def dictToExtension(self, d:dict, version:int=0):
        extensionTable = {}
        extensionTable[SetForceExtension.__name__] = SetForceExtension()
        extensionTable[LangevinExtension.__name__] = LangevinExtension()
        extensionTable[MoveExtension.__name__] = MoveExtension()
        extensionTable[ManualExtension.__name__] = ManualExtension()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in extensionTable.keys():
            raise RuntimeError(f"Unknown Extension class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(extensionTable[className])
        obj.fromDict(d, version)

        return obj