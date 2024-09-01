import copy 

from lammpsinputbuilder.fileIO import * 

class FileIOLoader():
    def __init__(self) -> None:
            pass

    def dictToFileIO(self, d:dict, version:int=0):
        fileIOTable = {}
        fileIOTable[ReaxBondFileIO.__name__] = ReaxBondFileIO()
        fileIOTable[DumpTrajectoryFileIO.__name__] = DumpTrajectoryFileIO()
        fileIOTable[XYZTrajectoryFileIO.__name__] = XYZTrajectoryFileIO()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in fileIOTable.keys():
            raise RuntimeError(f"Unknown FileIO class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(fileIOTable[className])
        obj.fromDict(d, version)

        return obj