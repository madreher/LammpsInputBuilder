"""Module implementing the FileIO class and its subclasses."""

from pathlib import Path
from typing import List
from enum import IntEnum
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.base import BaseObject



class FileIO(BaseObject):
    """
    Base class for FileIOs, a representation for lammps commands 
    producing trajectory files specifically. For command producing a 
    file only for the current state (ex: write_data), please use an Instruction 
    object instead of a FileIO.

    A FileIO has a scope and therfor must provide a way to declare the 
    computations, but also how to un-declare them. This is done by overriding
    the `add_do_commands()` and `add_undo_commands()` methods. Each subclass 
    implementing a new Extension must implement both these methods.

    This class should never be instantiated directly. Instead, the subclasses
    should implement the `add_do_commands()` and `add_undo_commands()` methods.
    """
    def __init__(self, fileio_name: str = "defaultFileIO") -> None:
        """
        Args:
            fileio_name (str): The name of the fileio. The name must be alpha numeric
                                and start with a letter

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(id_name=fileio_name)

    def get_fileio_name(self) -> str:
        """
        Get the name of the fileio.

        Returns:
            str: The name of the fileio
        """
        return super().get_id_name()

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the fileio.

        Returns:
            dict: The dictionary representation of the fileio
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Generate the commands for the fileio.

        Args:
            global_information (GlobalInformation): The global information object

        Returns:
            str: The commands for the fileio

        Raises:
            NotImplementedError: If the method is not implemented by the subclass
        """
        del global_information  # unused
        raise NotImplementedError((f"Method not implemented by class {__class__}. This method"
                                   " must be overridden by any subclasses of FileIO"))

    def add_undo_commands(self) -> str:
        """
        Generate the undo commands for the fileio.

        Returns:
            str: The undo commands for the fileio

        Raises:
            NotImplementedError: If the method is not implemented by the subclass
        """
        raise NotImplementedError((f"Method not implemented by class {__class__}. This method"
                                   " must be overridden by any subclasses of FileIO"))

    def get_associated_file_path(self) -> Path:
        """
        Get the path to the associated file.

        Returns:
            Path: The path to the associated file
        """
        return Path()

class DumpStyle(IntEnum):
    CUSTOM = 1
    XYZ = 2


class DumpTrajectoryFileIO(FileIO):
    """
    Writes trajectory files in custom or xyz styles. For other styles or 
    file formats, please refer to the ManualFileIO class instead.
    Lammps documentation: https://docs.lammps.org/dump.html
    """
    def __init__(
            self,
            fileio_name: str = "defaultDumpTrajectoryFileIO",
            style: DumpStyle = DumpStyle.CUSTOM,
            user_fields: List[str] = None,
            add_default_fields: bool = True,
            interval: int = 100,
            group: Group = AllGroup()) -> None:
        """
        Constructor for the DumpTrajectoryFileIO class. 
        Args:
            fileio_name (str): The name of the fileio. The name must be alpha numeric
                                and start with a letter
            style (DumpStyle): The style of the dump trajectory file
            user_fields (List[str]): The list of fields to include in the dump trajectory file. 
                                     Settings only used if the dump style is set to custom
            add_default_fields (bool): Add the default fields to the dump trajectory file. 
                                       Settings only used if the dump style is set to custom
            interval (int): The trajectory file will be written every n time steps
            group (Group): Writting the trajectory file for the atoms in this group

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
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
        """
        Get the list of fields to include in the dump trajectory file.

        Returns:
            List[str]: The list of fields to include in the dump trajectory file
        """
        return self.user_fields

    def get_add_default_fields(self) -> bool:
        """
        Get whether to add the default fields to the dump trajectory file.

        Returns:
            bool: Whether to add the default fields to the dump trajectory file
        """
        return self.add_default_fields

    def get_default_fields(self) -> List[str]:
        """
        Get the default fields to include in the dump trajectory file.

        Returns:
            List[str]: The default fields to include in the dump trajectory file
        """
        return self.default_fields

    def get_interval(self) -> int:
        """
        Get the trajectory output frequency.

        Returns:
            int: The trajectory file will be written every n time steps
        """
        return self.interval

    def get_group_name(self) -> str:
        """
        Get the name of the group to apply the fileio to.

        Returns:
            str: The name of the group to apply the fileio to
        """
        return self.group_name

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the dump trajectory fileio.

        Returns:
            dict: The dictionary representation of the dump trajectory fileio
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["user_fields"] = self.user_fields
        result["add_default_fields"] = self.add_default_fields
        result["interval"] = self.interval
        result["group_name"] = self.group_name
        result["style"] = self.style.value
        return result

    def from_dict(self, d: dict, version: int):
        """
        Load the dump trajectory fileio from a dictionary representation.

        Args:
            d (dict): The dictionary representation of the dump trajectory fileio
            version (int): The version of the dump trajectory fileio

        Returns:
            None
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.user_fields = d.get("user_fields", [])
        self.add_default_fields = d.get("add_default_fields", True)
        self.interval = d.get("interval", 100)
        self.group_name = d.get("group_name", AllGroup().get_group_name())
        self.style = DumpStyle(d.get("style", DumpStyle.CUSTOM.value))

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the dump trajectory.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
            
        Raises:
            RuntimeError: If "element" is part of the dump file custom fields, 
                           but the element table from the GlobalInformation is empty.
        """
        result = ""
        if self.style == DumpStyle.CUSTOM:
            result += (f"dump {self.get_fileio_name()} {self.group_name} custom "
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
            result += f"dump_modify {self.get_fileio_name()} sort id\n"
            if "element" in fields:
                if len(global_information.get_element_table()) == 0:
                    raise RuntimeError(
                        ("\'element\' is part of the dump file custom fields, "
                        "but the element table is empty. Unable to produce to "
"                       correct trajectory file."))
                result += f"dump_modify {self.get_fileio_name()} element"
                for elem in global_information.get_element_table().values():
                    result += f" {elem}"
                result += "\n"
        elif self.style == DumpStyle.XYZ:
            result += (f"dump {self.get_fileio_name()} {self.group_name} xyz "
                    f"{self.interval} {self.get_associated_file_path()}\n")
        else:
            raise ValueError(f"Invalid dump style {self.style}.")

        return result

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to undo the dump trajectory.

        Returns:
            str: Lammps command(s)
        """
        return f"undump {self.get_fileio_name()}\n"

    def get_associated_file_path(self) -> Path:
        """
        Get the name to the associated file. The file is located
        is the job folder.

        Returns:
            Path: The name to the associated file
        """
        if self.style == DumpStyle.CUSTOM:
            return Path("dump." + self.get_fileio_name() + ".lammpstrj")
        if self.style == DumpStyle.XYZ:
            return Path("dump." + self.get_fileio_name() + ".xyz")

        raise ValueError(f"Invalid dump style {self.style}.")


class ReaxBondFileIO(FileIO):
    """
    Writes trajectory files for the bond during a reax simulation. 
    Lammps documentation: https://docs.lammps.org/fix_reaxff_bonds.html
    """
    def __init__(
            self,
            fileio_name: str = "defaultReaxBondFileIO",
            group: Group = AllGroup(),
            interval: int = 100) -> None:
        """
        Constructor for the ReaxBondFileIO class. 
        Args:
            fileio_name (str): The name of the fileio. The name must be alpha numeric
                                and start with a letter
            group (Group): Writting the bond file for the atoms in this group
            interval (int): The trajectory file will be written every n time steps

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(fileio_name=fileio_name)
        self.group_name = group.get_group_name()
        self.interval = interval

    def get_group_name(self) -> str:
        """
        Get the name of the group to apply the fileio to.

        Returns:
            str: The name of the group
        """
        return self.group_name

    def get_interval(self) -> int:
        """
        Get the trajectory output frequency.

        Returns:
            int: The trajectory file will be written every n time steps
        """
        return self.interval

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the dump trajectory fileio.

        Returns:
            dict: The dictionary representation of the dump trajectory fileio
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["group_name"] = self.group_name
        result["interval"] = self.interval
        return result

    def from_dict(self, d: dict, version: int):
        """
        Load the dump trajectory fileio from a dictionary representation.

        Args:
            d (dict): The dictionary representation of the dump trajectory fileio
            version (int): The version of the dump trajectory fileio

        Returns:
            None
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.group_name = d.get("group_name", AllGroup().get_group_name())
        self.interval = d.get("interval", 100)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to write the reaxff/bonds trajectory.

        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        return (f"fix {self.get_fileio_name()} {self.group_name} reaxff/bonds "
                f"{self.interval} bonds.{self.get_fileio_name()}.txt\n")

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to undo the reaxff/bonds trajectory.

        Returns:
            str: Lammps command(s)
        """
        return f"unfix {self.get_fileio_name()}\n"

    def get_associated_file_path(self) -> Path:
        """
        Get the name to the associated file. The file is located
        is the job folder.

        Returns:
            Path: The name to the associated file
        """
        return Path(f"bonds.{self.get_fileio_name()}.txt")


class ThermoFileIO(FileIO):
    """
    Update the thermo output configuration.
    IMPORTANT: Unlike the other FileIO classes, this class doesn't have a scope and 
    always apply to the entire system.
    Lammps documentation: https://docs.lammps.org/fix_reaxff_bonds.html
    """
    def __init__(
            self,
            fileio_name: str = "defaultThermoFileIO",
            interval: int = 10,
            add_default_fields: bool = True,
            user_fields: List[str] = None) -> None:
        """
        Constructor for the ThermoFileIO class. 
        Args:
            fileio_name (str): The name of the fileio. The name must be alpha numeric
                                and start with a letter
            interval (int): The trajectory file will be written every n time steps
            add_default_fields (bool): Add the default fields to the thermo trajectory file
            user_fields (List[str]): List of fields to include in the thermo output

        Returns:
            None

        """
        super().__init__(fileio_name=fileio_name)
        self.interval = interval
        if user_fields is None:
            self.user_fields = []
        else:
            self.user_fields = user_fields
        self.add_default_fields = add_default_fields
        self.default_fields = ["step", "temp", "pe", "ke", "etotal", "press"]

    def set_user_fields(self, user_fields: List[str]):
        """
        Set the list of fields to include in the thermo output in addition 
        to the default fields if enabled.

        Args:
            user_fields (List[str]): List of fields to include in the thermo output
        Returns:
            None
        """
        self.user_fields = user_fields

    def get_user_fields(self) -> List[str]:
        """
        Get the list of fields provided by the user to include in the thermo output.

        Returns:
            List[str]: The list of fields to include in the thermo output
        """
        return self.user_fields

    def get_add_default_fields(self) -> bool:
        """
        Get whether to add the default fields to the thermo output.

        Returns:
            bool: Whether to add the default fields to the thermo output
        """
        return self.add_default_fields

    def set_add_default_fields(self, add_default_fields: bool):
        """
        Set whether to add the default fields to the thermo output.

        Args:
            add_default_fields (bool): Whether to add the default fields to the thermo output
        Returns:
            None
        """
        self.add_default_fields = add_default_fields

    def get_default_fields(self) -> List[str]:
        """
        Get the default fields to include in the thermo output.

        Returns:
            List[str]: The default fields to include in the thermo output
        """
        return self.default_fields

    def get_interval(self) -> int:
        """
        Get the trajectory output frequency.

        Returns:
            int: The trajectory file will be written every n time steps
        """
        return self.interval

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the dump trajectory fileio.

        Returns:
            dict: The dictionary representation of the dump trajectory fileio
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["user_fields"] = self.user_fields
        result["add_default_fields"] = self.add_default_fields
        result["interval"] = self.interval
        return result

    def from_dict(self, d: dict, version: int):
        """
        Load the dump trajectory fileio from a dictionary representation.

        Args:
            d (dict): The dictionary representation of the dump trajectory fileio
            version (int): The version of the dump trajectory fileio

        Returns:
            None
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.user_fields = d.get("user_fields", [])
        self.add_default_fields = d.get("add_default_fields", True)
        self.interval = d.get("interval", 10)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Add the do commands to update the output of thermo output.

        Args:
            global_information (GlobalInformation): The global information object

        Returns:
            str: The do commands for the dump trajectory fileio
        """
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
        """
        Nothing to do in this case.

        Returns:
            str: empty string
        """
        return ""

    def get_associated_file_path(self) -> Path:
        """
        File containing the thermo output.
        The output of thermo is always written to the file lammps.log in the job folder.
        """
        return Path("lammps.log")


class ManualFileIO(FileIO):
    """
    A ManualFileIO is a way to add manual commands to the workflow
    which will follow the same execution order as the other fileios.
    It should be used for cases where the user needs a command or set of commands
    not currently supported by another fileio. In this case, the user is 
    responsible for adding the commands to declare and remove the fileio.

    If a FileIO is missing from the library, please submit an issue to the Github repository.
    """

    def __init__(
            self,
            fileio_name: str = "defaultManualFileIO",
            do_cmd: str = "",
            undo_cmd: str = "",
            associated_file_path: str = "") -> None:  
        """
        Constructor
        Args:
            fileio_name (str): The name of the fileio. The name must be alpha numeric
                                and start with a letter
            do_cmd (str): The command to execute when the fileio is added
            undo_cmd (str): The command to execute when the fileio is removed
            associated_file_path (str): The path to the file associated with the fileio
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(fileio_name=fileio_name)
        self.do_cmd = do_cmd
        self.undo_cmd = undo_cmd
        self.associated_file_path = associated_file_path

    def get_do_cmd(self) -> str:
        """
        Get the Lammps commands to declare the fileio.

        Returns:
            str: Lammps command(s)
        """
        return self.do_cmd

    def get_undo_cmd(self) -> str:
        """
        Get the Lammps commands to remove the fileio.

        Returns:
            str: Lammps command(s)
        """
        return self.undo_cmd

    def get_associated_file_path(self) -> Path:
        """
        Get the path to the associated file.

        Returns:
            Path: The path to the associated file
        """
        return Path(self.associated_file_path)

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the fileio.

        Returns:
            dict: The dictionary representation of the fileio
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        result["associated_file_path"] = self.associated_file_path
        return result

    def from_dict(self, d: dict, version: int):
        """
        Load the dump trajectory fileio from a dictionary representation.

        Args:
            d (dict): The dictionary representation of the fileio
            version (int): The version of the fileio

        Returns:
            None    
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.do_cmd = d.get("do_cmd", "")
        self.undo_cmd = d.get("undo_cmd", "")
        self.associated_file_path = d.get("associated_file_path", "")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Add the do commands to the workflow.

        Args:
            global_information (GlobalInformation): The global information object

        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        if self.do_cmd.endswith("\n"):
            return self.do_cmd

        return self.do_cmd + "\n"

    def add_undo_commands(self) -> str:
        """
        Add the undo commands to the workflow.

        Returns:
            str: Lammps command(s)
        """
        if self.undo_cmd.endswith("\n"):
            return self.undo_cmd

        return self.undo_cmd + "\n"
