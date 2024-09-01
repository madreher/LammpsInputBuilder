from pathlib import Path

class FileIO:

    def __init__(self):
        pass

    def toDict(self) -> dict:
        return {}

    def fromDict(self, d: dict, version: int):
        pass

    def addDoCommands(self) -> str:
        return ""
    
    def addUndoCommands(self) -> str:
        return ""
    
    def getAssociatedFilePath(self) -> Path:
        return Path()
    
class XYZTrajectoryFileIO(FileIO):

    def __init__(self):
        super().__init__()

    def toDict(self) -> dict:
        pass    

    def fromDict(self, d: dict, version: int):
        pass    

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

    def getAssociatedFilePath(self) -> Path:
        return Path()
    

class DumpTrajectoryFileIO(FileIO):

    def __init__(self):
        super().__init__()

    def toDict(self) -> dict:
        pass    

    def fromDict(self, d: dict, version: int):
        pass    

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

    def getAssociatedFilePath(self) -> Path:
        return Path()

