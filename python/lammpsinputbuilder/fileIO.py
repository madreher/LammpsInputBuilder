"""Module implementing the FileIO class and its subclasses."""

from pathlib import Path
from typing import List
from enum import Enum
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.types import GlobalInformation



class FileIO:

    def __init__(self, fileio_name: str = "defaultFileIO") -> None:
        self.fileio_name = fileio_name

    def getFileIOName(self) -> str:
        return self.fileio_name

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["fileio_name"] = self.fileio_name
        return result

    def from_dict(self, d: dict, version: int):
        self.fileio_name = d.get("fileio_name", "defaultFileIO")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""

    def getAssociatedFilePath(self) -> Path:
        return Path()


class XYZTrajectoryFileIO(FileIO):

    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        pass

    def from_dict(self, d: dict, version: int):
        pass

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""

    def getAssociatedFilePath(self) -> Path:
        return Path()


class DumpStyle(Enum):
    CUSTOM = 1,
    XYZ = 2


class DumpTrajectoryFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultDumpTrajectoryFileIO",
            style: DumpStyle = DumpStyle.CUSTOM,
            userFields: List[str] = [],
            addDefaultFields: bool = True,
            interval: int = 100,
            group: Group = AllGroup()) -> None:
        super().__init__(fileio_name=fileio_name)
        self.userFields = userFields
        self.addDefaultFields = addDefaultFields
        self.defaultFields = ["id", "type", "x", "y", "z"]
        self.interval = interval
        self.group_name = group.get_group_name()
        self.style = style

    def getUserFields(self) -> List[str]:
        return self.userFields

    def getAddDefaultFields(self) -> bool:
        return self.addDefaultFields

    def getDefaultFields(self) -> List[str]:
        return self.defaultFields

    def getInterval(self) -> int:
        return self.interval

    def get_group_name(self) -> str:
        return self.group_name

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["userFields"] = self.userFields
        result["addDefaultFields"] = self.addDefaultFields
        result["interval"] = self.interval
        result["group_name"] = self.group_name
        result["style"] = self.style.value
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.userFields = d.get("userFields", [])
        self.addDefaultFields = d.get("addDefaultFields", True)
        self.interval = d.get("interval", 100)
        self.group_name = d.get("group_name", AllGroup().get_group_name())
        self.style = DumpStyle(d.get("style", DumpStyle.CUSTOM.value))
        pass

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        if self.style == DumpStyle.CUSTOM:
            result += f"dump {self.fileio_name} {self.group_name} custom {self.interval} {self.getAssociatedFilePath()}"
            fields = []
            if self.addDefaultFields:
                fields.extend(self.defaultFields)
            if len(self.userFields) > 0:
                for field in self.userFields:
                    if field not in fields:
                        fields.append(field)

            # Ensure that we always have the id to identify the atoms
            if "id" not in fields:
                fields.insert(0, "id")

            for field in fields:
                result += f" {field}"
            result += "\n"
            result += f"dump_modify {self.fileio_name} sort id\n"
            if "element" in fields:
                if len(global_information.getElementTable()) == 0:
                    raise RuntimeError(
                        "\'element\' is part of the dump file custom fields, but the element table is empty. Unable to produce to correct trajectory file.")
                result += f"dump_modify {self.fileio_name} element"
                for elem in global_information.getElementTable().values():
                    result += f" {elem}"
                result += "\n"
        elif self.style == DumpStyle.XYZ:
            result += f"dump {self.fileio_name} {self.group_name} xyz {self.interval} {self.getAssociatedFilePath()}\n"
        else:
            raise ValueError(f"Invalid dump style {self.style}.")

        return result

    def add_undo_commands(self) -> str:
        return f"undump {self.fileio_name}\n"

    def getAssociatedFilePath(self) -> Path:
        if self.style == DumpStyle.CUSTOM:
            return Path("dump." + self.fileio_name + ".lammpstrj")
        elif self.style == DumpStyle.XYZ:
            return Path("dump." + self.fileio_name + ".xyz")
        else:
            raise ValueError(f"Invalid dump style {self.style}.")


class ReaxBondFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultReaxBondFileIO",
            group: Group = AllGroup(),
            interval: int = 100) -> None:
        super().__init__(fileio_name=fileio_name)
        self.group_name = group.get_group_name()
        self.interval = interval

    def get_group_name(self) -> str:
        return self.group_name

    def getInterval(self) -> int:
        return self.interval

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["fileio_name"] = self.fileio_name
        result["group_name"] = self.group_name
        result["interval"] = self.interval
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.fileio_name = d.get("fileio_name", "defaultReaxBondFileIO")
        self.group_name = d.get("group_name", AllGroup().get_group_name())
        self.interval = d.get("interval", 100)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return f"fix {self.fileio_name} {self.group_name} reaxff/bonds {self.interval} bonds.{self.fileio_name}.txt\n"

    def add_undo_commands(self) -> str:
        return f"unfix {self.fileio_name}\n"

    def getAssociatedFilePath(self) -> Path:
        return Path(f"bonds.{self.fileio_name}.txt")


class ThermoFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultThermoFileIO",
            interval: int = 10,
            addDefaultFields: bool = True,
            userFields: List[str] = []) -> None:  # ) -> None:
        super().__init__(fileio_name=fileio_name)
        self.interval = interval
        self.userFields = userFields
        self.addDefaultFields = addDefaultFields
        self.defaultFields = ["step", "temp", "pe", "ke", "etotal", "press"]

    def setUserFields(self, userFields: List[str]):
        self.userFields = userFields

    def getUserFields(self) -> List[str]:
        return self.userFields

    def getAddDefaultFields(self) -> bool:
        return self.addDefaultFields

    def setAddDefaultFields(self, addDefaultFields: bool):
        self.addDefaultFields = addDefaultFields

    def getDefaultFields(self) -> List[str]:
        return self.defaultFields

    def getInterval(self) -> int:
        return self.interval

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["userFields"] = self.userFields
        result["addDefaultFields"] = self.addDefaultFields
        result["interval"] = self.interval
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.userFields = d.get("userFields", [])
        self.addDefaultFields = d.get("addDefaultFields", True)
        self.interval = d.get("interval", 10)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        result += f"thermo {self.interval}\n"
        fields = []
        if self.addDefaultFields:
            fields.extend(self.defaultFields)
        if len(self.userFields) > 0:
            for field in self.userFields:
                if field not in self.defaultFields:
                    fields.append(field)
        result += f"thermo_style custom"
        for field in fields:
            result += f" {field}"
        result += "\n"
        return result

    def add_undo_commands(self) -> str:
        return ""

    def getAssociatedFilePath(self) -> Path:
        return Path("lammps.log")


class ManualFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultManualFileIO",
            doCmd: str = "",
            undoCmd: str = "",
            associatedFilePath: str = "") -> None:  # ) -> None: # ) -> None:
        super().__init__(fileio_name=fileio_name)
        self.doCmd = doCmd
        self.undoCmd = undoCmd
        self.associatedFilePath = associatedFilePath

    def getDoCmd(self) -> str:
        return self.doCmd

    def getUndoCmd(self) -> str:
        return self.undoCmd

    def getAssociatedFilePath(self) -> Path:
        return Path(self.associatedFilePath)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["doCmd"] = self.doCmd
        result["undoCmd"] = self.undoCmd
        result["associatedFilePath"] = self.associatedFilePath
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.doCmd = d.get("doCmd", "")
        self.undoCmd = d.get("undoCmd", "")
        self.associatedFilePath = d.get("associatedFilePath", "")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        if self.doCmd.endswith("\n"):
            return self.doCmd
        else:
            return self.doCmd + "\n"

    def add_undo_commands(self) -> str:
        if self.undoCmd.endswith("\n"):
            return self.undoCmd
        else:
            return self.undoCmd + "\n"

    def getAssociatedFilePath(self) -> Path:
        return Path(self.associatedFilePath)
