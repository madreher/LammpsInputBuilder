"""Module implementing the FileIO class and its subclasses."""

from pathlib import Path
from typing import List
from enum import Enum
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.types import GlobalInformation



class FileIO:

    def __init__(self, fileio_name: str = "defaultFileIO") -> None:
        self.fileio_name = fileio_name

    def get_fileio_name(self) -> str:
        return self.fileio_name

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["fileio_name"] = self.fileio_name
        return result

    def from_dict(self, d: dict, version: int):
        del version  # unused
        self.fileio_name = d.get("fileio_name", "defaultFileIO")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        del global_information  # unused
        return ""

    def add_undo_commands(self) -> str:
        return ""

    def get_associated_file_path(self) -> Path:
        return Path()

class DumpStyle(Enum):
    CUSTOM = 1
    XYZ = 2


class DumpTrajectoryFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultDumpTrajectoryFileIO",
            style: DumpStyle = DumpStyle.CUSTOM,
            user_fields: List[str] = None,
            add_default_fields: bool = True,
            interval: int = 100,
            group: Group = AllGroup()) -> None:
        super().__init__(fileio_name=fileio_name)
        if user_fields is None:
            self.user_fields = []
        else:
            self.user_fields = user_fields
        self.add_default_fields = add_default_fields
        self.default_fields = ["id", "type", "x", "y", "z"]
        self.interval = interval
        self.group_name = group.get_group_name()
        self.style = style

    def get_user_fields(self) -> List[str]:
        return self.user_fields

    def get_add_default_fields(self) -> bool:
        return self.add_default_fields

    def get_default_fields(self) -> List[str]:
        return self.default_fields

    def get_interval(self) -> int:
        return self.interval

    def get_group_name(self) -> str:
        return self.group_name

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["user_fields"] = self.user_fields
        result["add_default_fields"] = self.add_default_fields
        result["interval"] = self.interval
        result["group_name"] = self.group_name
        result["style"] = self.style.value
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.user_fields = d.get("user_fields", [])
        self.add_default_fields = d.get("add_default_fields", True)
        self.interval = d.get("interval", 100)
        self.group_name = d.get("group_name", AllGroup().get_group_name())
        self.style = DumpStyle(d.get("style", DumpStyle.CUSTOM.value))

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        if self.style == DumpStyle.CUSTOM:
            result += (f"dump {self.fileio_name} {self.group_name} custom "
                    f"{self.interval} {self.get_associated_file_path()}")
            fields = []
            if self.add_default_fields:
                fields.extend(self.default_fields)
            if len(self.user_fields) > 0:
                for field in self.user_fields:
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
                if len(global_information.get_element_table()) == 0:
                    raise RuntimeError(
                        ("\'element\' is part of the dump file custom fields, "
                        "but the element table is empty. Unable to produce to "
"                       correct trajectory file."))
                result += f"dump_modify {self.fileio_name} element"
                for elem in global_information.get_element_table().values():
                    result += f" {elem}"
                result += "\n"
        elif self.style == DumpStyle.XYZ:
            result += (f"dump {self.fileio_name} {self.group_name} xyz "
                    f"{self.interval} {self.get_associated_file_path()}\n")
        else:
            raise ValueError(f"Invalid dump style {self.style}.")

        return result

    def add_undo_commands(self) -> str:
        return f"undump {self.fileio_name}\n"

    def get_associated_file_path(self) -> Path:
        if self.style == DumpStyle.CUSTOM:
            return Path("dump." + self.fileio_name + ".lammpstrj")
        if self.style == DumpStyle.XYZ:
            return Path("dump." + self.fileio_name + ".xyz")

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

    def get_interval(self) -> int:
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
        return (f"fix {self.fileio_name} {self.group_name} reaxff/bonds "
                f"{self.interval} bonds.{self.fileio_name}.txt\n")

    def add_undo_commands(self) -> str:
        return f"unfix {self.fileio_name}\n"

    def get_associated_file_path(self) -> Path:
        return Path(f"bonds.{self.fileio_name}.txt")


class ThermoFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultThermoFileIO",
            interval: int = 10,
            add_default_fields: bool = True,
            user_fields: List[str] = None) -> None:  # ) -> None:
        super().__init__(fileio_name=fileio_name)
        self.interval = interval
        if user_fields is None:
            self.user_fields = []
        else:
            self.user_fields = user_fields
        self.add_default_fields = add_default_fields
        self.default_fields = ["step", "temp", "pe", "ke", "etotal", "press"]

    def set_user_fields(self, user_fields: List[str]):
        self.user_fields = user_fields

    def get_user_fields(self) -> List[str]:
        return self.user_fields

    def get_add_default_fields(self) -> bool:
        return self.add_default_fields

    def set_add_default_fields(self, add_default_fields: bool):
        self.add_default_fields = add_default_fields

    def get_default_fields(self) -> List[str]:
        return self.default_fields

    def get_interval(self) -> int:
        return self.interval

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["user_fields"] = self.user_fields
        result["add_default_fields"] = self.add_default_fields
        result["interval"] = self.interval
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.user_fields = d.get("user_fields", [])
        self.add_default_fields = d.get("add_default_fields", True)
        self.interval = d.get("interval", 10)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        del global_information  # unused
        result = ""
        result += f"thermo {self.interval}\n"
        fields = []
        if self.add_default_fields:
            fields.extend(self.default_fields)
        if len(self.user_fields) > 0:
            for field in self.user_fields:
                if field not in self.default_fields:
                    fields.append(field)
        result += "thermo_style custom"
        for field in fields:
            result += f" {field}"
        result += "\n"
        return result

    def add_undo_commands(self) -> str:
        return ""

    def get_associated_file_path(self) -> Path:
        return Path("lammps.log")


class ManualFileIO(FileIO):

    def __init__(
            self,
            fileio_name: str = "defaultManualFileIO",
            do_cmd: str = "",
            undo_cmd: str = "",
            associated_file_path: str = "") -> None:  # ) -> None: # ) -> None:
        super().__init__(fileio_name=fileio_name)
        self.do_cmd = do_cmd
        self.undo_cmd = undo_cmd
        self.associated_file_path = associated_file_path

    def get_do_cmd(self) -> str:
        return self.do_cmd

    def get_undo_cmd(self) -> str:
        return self.undo_cmd

    def get_associated_file_path(self) -> Path:
        return Path(self.associated_file_path)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        result["associated_file_path"] = self.associated_file_path
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.do_cmd = d.get("do_cmd", "")
        self.undo_cmd = d.get("undo_cmd", "")
        self.associated_file_path = d.get("associated_file_path", "")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        del global_information  # unused
        if self.do_cmd.endswith("\n"):
            return self.do_cmd

        return self.do_cmd + "\n"

    def add_undo_commands(self) -> str:
        if self.undo_cmd.endswith("\n"):
            return self.undo_cmd

        return self.undo_cmd + "\n"
