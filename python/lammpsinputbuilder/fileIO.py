from pathlib import Path
from typing import List
from lammpsinputbuilder.group import Group, AllGroup

class FileIO:

    def __init__(self, fileIOName: str = "defaultFileIO") -> None:
        self.fileIOName = fileIOName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["fileIOName"] = self.fileIOName
        return result

    def fromDict(self, d: dict, version: int):
        self.fileIOName = d.get("fileIOName", "defaultFileIO")

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

    def __init__(self, fileIOName: str = "defaultDumpTrajectoryFileIO", userFields: List[str] = [], addDefaultFields: bool = True, interval: int = 100, group: Group = AllGroup()) -> None:
        super().__init__(fileIOName=fileIOName)
        self.userFields = userFields
        self.addDefaultFields = addDefaultFields
        self.defaultFields = ["id", "type", "x", "y", "z"]
        self.interval = interval
        self.groupName = group.getGroupName()

    def toDict(self) -> dict:
        result  = super().toDict()
        result["class"] = self.__class__.__name__ 
        result["userFields"] = self.userFields
        result["addDefaultFields"] = self.addDefaultFields
        result["interval"] = self.interval
        result["group"] = self.groupName
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.userFields = d.get("userFields", [])
        self.addDefaultFields = d.get("addDefaultFields", True)
        self.interval = d.get("interval", 100)
        self.groupName = d.get("group", AllGroup().getGroupName())
        pass    

    def addDoCommands(self) -> str:
        result = ""
        result += f"dump {self.fileIOName} {self.groupName} custom {self.interval} dump.{self.fileIOName}.lammpstrj"
        fields = []
        if self.addDefaultFields:
            fields.extend(self.defaultFields)
        fields.extend(self.userFields)

        # Ensure that we always have the id to identify the atoms
        if "id" not in fields:
            fields.insert(0, "id")

        for field in fields:
            result += f" {field}"
        result += "\n"
        result += f"dump_modify {self.fileIOName} sort id\n"
        return result

    def addUndoCommands(self) -> str:
        return f"undump {self.fileIOName}\n"

    def getAssociatedFilePath(self) -> Path:
        return Path(self.fileIOName + ".lammpstrj")
    

class ReaxBondFileIO(FileIO):

    def __init__(self, fileIOName: str = "defaultReaxBondFileIO", group: Group = AllGroup(), interval: int = 100) -> None:
        super().__init__()
        self.fileIOName = fileIOName
        self.groupName = group.getGroupName()
        self.interval = interval

    def toDict(self) -> dict:
        result  = super().toDict()
        result["class"] = self.__class__.__name__ 
        result["fileIOName"] = self.fileIOName
        result["group"] = self.groupName
        result["interval"] = self.interval
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.fileIOName = d.get("fileIOName", "defaultReaxBondFileIO")
        self.groupName = d.get("group", AllGroup().getGroupName())
        self.interval = d.get("interval", 100)   

    def addDoCommands(self) -> str:
        return f"fix {self.fileIOName} {self.groupName} reaxff/bonds {self.interval} bonds.{self.fileIOName}.txt\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.fileIOName}\n"

    def getAssociatedFilePath(self) -> Path:
        return Path(f"bonds.{self.fileIOName}.txt")
    
class ThermoFileIO(FileIO):

    def __init__(self, fileIOName: str = "defaultThermoFileIO", interval: int = 10, addDefaultFields: bool = True, userFields: List[str] = []) -> None: # ) -> None:
        super().__init__(fileIOName=fileIOName)
        self.interval = interval
        self.userFields = userFields
        self.addDefaultFields = addDefaultFields
        self.defaultFields = ["step", "temp", "pe", "ke", "etotal", "press"]

    def setUserFields(self, userFields: List[str]):
        self.userFields = userFields

    def getUserFields(self) -> List[str]:
        return self.userFields
    
    def setAddDefaultFields(self, addDefaultFields: bool):
        self.addDefaultFields = addDefaultFields

    def toDict(self) -> dict:
        result  = super().toDict()
        result["class"] = self.__class__.__name__ 
        result["userFields"] = self.userFields
        result["addDefaultFields"] = self.addDefaultFields
        result["interval"] = self.interval
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.userFields = d.get("userFields", [])
        self.addDefaultFields = d.get("addDefaultFields", True)
        self.interval = d.get("interval", 10)

    def addDoCommands(self) -> str:
        result = ""
        result += f"thermo {self.interval}\n"
        fields = []
        if self.addDefaultFields:
            fields.extend(self.defaultFields)
        fields.extend(self.userFields)
        result += f"thermo_style custom"
        for field in fields:
            result += f" {field}"
        result += "\n"
        return result

    def addUndoCommands(self) -> str:
        return ""

    def getAssociatedFilePath(self) -> Path:
        return Path("lammps.log")

