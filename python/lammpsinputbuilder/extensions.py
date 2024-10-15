"""Module containing the definition of the Extension class and its subclasses."""

from lammpsinputbuilder.group import AllGroup, Group
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity, \
    ForceQuantity, VelocityQuantity
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.instructions import Instruction
from lammpsinputbuilder.base import BaseObject


class Extension(BaseObject):
    """
    Base class for Lammps method adding computations during the timestepping process
    in addition to the time integration or geometry optimization process.
    
    An extension has a scope, and therfor must provide a way to declare the 
    computations, but also how to un-declare them. This is done by overriding
    the `add_do_commands()` and `add_undo_commands()` methods. Each subclass 
    implementing a new Extension must implement both these methods.

    This class should never be instantiated directly. Instead, the subclasses
    should implement the `add_do_commands()` and `add_undo_commands()` methods.
    """
    def __init__(self, extension_name: str = "defaultExtension") -> None:
        """
        Args:
            extension_name (str): The name of the extension. The name must be alpha numeric
                                and start with a letter

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(id_name=extension_name)

    def to_dict(self) -> dict:
        """
        Return the dictionary representation of the extension

        Returns:
            dict: The dictionary representation of the extension
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def get_extension_name(self) -> str:
        """
        Return the name of the extension

        Returns:
            str: The name of the extension
        """
        return super().get_id_name()

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the extension.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)

        Raises:
            NotImplementedError: If the method is not implemented by the subclass
        """

        del global_information  # unused
        raise NotImplementedError((f"Method not implemented by class {__class__}. This method"
                                   " must be overridden by any subclasses of Extension"))

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to remove the extension.

        Returns:
            str: Lammps command(s)

        Raises:
            NotImplementedError: If the method is not implemented by the subclass
        """
        raise NotImplementedError((f"Method not implemented by class {__class__}. This method"
                                   " must be overridden by any subclasses of Extension"))


class LangevinExtension(Extension):
    """
    Creating a langevin thermostat on a group of atoms from a starting temperature 
    to and end temperature until the extension is removed. 

    Lammps documentation: https://docs.lammps.org/fix_langevin.html
    """
    def __init__(
            self,
            extension_name: str = "defaultLangevinExtension",
            group: Group = AllGroup(),
            start_temp: TemperatureQuantity = TemperatureQuantity(
                1.0,
                "K"),
            end_temp: TemperatureQuantity = TemperatureQuantity(
                1.0,
                "K"),
            damp: TimeQuantity = TimeQuantity(
                10.0,
                "ps"),
            seed: int = 122345) -> None:
        """
        Constructor
        Args:
            extension_name (str): The name of the extension. The name must be alpha numeric
                                and start with a letter
            group (Group): The group to apply the extension to
            start_temp (TemperatureQuantity): The initial temperature
            end_temp (TemperatureQuantity): The final temperature
            damp (TimeQuantity): The damping factor
            seed (int): The seed for the random number generator
        Raise:
            ValueError: If the seed is a negative value
        """
        super().__init__(extension_name=extension_name)
        self.group = group.get_group_name()
        self.start_temp = start_temp
        self.end_temp = end_temp
        self.damp = damp
        if seed < 0:
            raise ValueError("Seed must be a positive integer.")
        self.seed = seed

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the extension.

        Returns:
            dict: The dictionary representation of the extension.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["group_name"] = self.group
        result["start_temp"] = self.start_temp.to_dict()
        result["end_temp"] = self.end_temp.to_dict()
        result["damp"] = self.damp.to_dict()
        result["seed"] = self.seed
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the seed is a negative value
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.group = d.get("group_name", AllGroup().get_group_name())
        self.start_temp = TemperatureQuantity()
        self.start_temp.from_dict(d["start_temp"], version)
        self.end_temp = TemperatureQuantity()
        self.end_temp.from_dict(d["end_temp"], version)
        self.damp = TimeQuantity()
        self.damp.from_dict(d["damp"], version)
        self.seed = d.get("seed", 122345)
        if self.seed < 0:
            raise ValueError("Seed must be a positive integer.")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the extension.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
        """
        return (f"fix {self.get_extension_name()} {self.group} langevin "
                f"{self.start_temp.convert_to(global_information.get_unit_style())} "
                f"{self.end_temp.convert_to(global_information.get_unit_style())} "
                f"{self.damp.convert_to(global_information.get_unit_style())} {self.seed}\n")

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to remove the extension.

        Returns:
            str: Lammps command(s)
        """
        return f"unfix {self.get_extension_name()}\n"


class SetForceExtension(Extension):
    """
    Set the force components to a fixed value on a group of atoms 
    until the extension is removed.

    Lammps documentation: https://docs.lammps.org/fix_setforce.html
    """
    def __init__(
        self,
        extension_name: str = "defaultSetForceExtension",
        group: Group = AllGroup(),
        fx: ForceQuantity = ForceQuantity(
            0.0,
            "(kcal/mol)/angstrom"),
        fy: ForceQuantity = ForceQuantity(
            0.0,
            "(kcal/mol)/angstrom"),
            fz: ForceQuantity = ForceQuantity(
                0.0,
            "(kcal/mol)/angstrom")) -> None:
        """
        Constructor
        Args:
            extension_name (str): The name of the extension. The name must be alpha numeric
                                and start with a letter
            group (Group): The group to apply the extension to
            fx (ForceQuantity): The x force
            fy (ForceQuantity): The y force
            fz (ForceQuantity): The z force
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(extension_name=extension_name)
        self.group = group.get_group_name()
        self.fx = fx
        self.fy = fy
        self.fz = fz

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the extension.

        Returns:
            dict: The dictionary representation of the extension.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["group_name"] = self.group
        result["fx"] = self.fx.to_dict()
        result["fy"] = self.fy.to_dict()
        result["fz"] = self.fz.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.group = d.get("group_name", AllGroup().get_group_name())
        self.fx = ForceQuantity()
        if "fx" in d:
            self.fx.from_dict(d["fx"], version)
        self.fy = ForceQuantity()
        if "fy" in d:
            self.fy.from_dict(d["fy"], version)
        self.fz = ForceQuantity()
        if "fz" in d:
            self.fz.from_dict(d["fz"], version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the extension. Force values are 
        converted to the unit set declared in the global information.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
        """
        return (f"fix {self.get_extension_name()} {self.group} setforce "
            f"{self.fx.convert_to(global_information.get_unit_style())} "
            f"{self.fy.convert_to(global_information.get_unit_style())} "
            f"{self.fz.convert_to(global_information.get_unit_style())}\n")

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to remove the extension.

        Returns:
            str: Lammps command(s)
        """
        return f"unfix {self.get_extension_name()}\n"


class MoveExtension(Extension):
    """
    Move the atoms in a group at a given velocity until the extension is removed.
    Currently, only the linear style is supported. If you want to use other
    styles, use the ManualExtension.

    Lammps documentation: https://docs.lammps.org/fix_move.html
    """
    def __init__(
        self,
        extension_name: str = "defaultMoveExtension",
        group: Group = AllGroup(),
        vx: VelocityQuantity = VelocityQuantity(
            0.0,
            "angstrom/ps"),
        vy: VelocityQuantity = VelocityQuantity(
            0.0,
            "angstrom/ps"),
        vz: VelocityQuantity = VelocityQuantity(
            0.0,
            "angstrom/ps")) -> None:
        """
        Constructor
        Args:
            extension_name (str): The name of the extension. The name must be alpha numeric
                                and start with a letter
            group (Group): The group to apply the extension to
            vx (VelocityQuantity): The x velocity
            vy (VelocityQuantity): The y velocity
            vz (VelocityQuantity): The z velocity
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(extension_name=extension_name)
        self.group = group.get_group_name()
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the extension.

        Returns:
            dict: The dictionary representation of the extension.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["group_name"] = self.group
        result["vx"] = self.vx.to_dict()
        result["vy"] = self.vy.to_dict()
        result["vz"] = self.vz.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.group = d.get("group_name", AllGroup().get_group_name())
        self.vx = VelocityQuantity()
        if "vx" in d:
            self.vx.from_dict(d["vx"], version)
        self.vy = VelocityQuantity()
        if "vy" in d:
            self.vy.from_dict(d["vy"], version)
        self.vz = VelocityQuantity()
        if "vz" in d:
            self.vz.from_dict(d["vz"], version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the extension. Velocity values are 
        converted to the unit set declared in the global information.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
        """
        return (f"fix {self.get_extension_name()} {self.group} move linear "
            f"{self.vx.convert_to(global_information.get_unit_style())} "
            f"{self.vy.convert_to(global_information.get_unit_style())} "
            f"{self.vz.convert_to(global_information.get_unit_style())}\n")

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to remove the extension.

        Returns:
            str: Lammps command(s)
        """
        return f"unfix {self.get_extension_name()}\n"


class InstructionExtension(Extension):
    """
    Adapter to use an Instruction as an Extension. This class should be used for 
    cases where an instruction has to be executed between two extensions declarations.
    The Instruction command will be written when the add_do_commands method is called.
    """
    def __init__(self, instruction: Instruction = Instruction()) -> None:
        """
        Constructor
        Args:
            instruction (Instruction): The instruction to process instead of an extension
        """
        super().__init__(instruction.get_instruction_name())
        self.instruction = instruction

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the extension.

        Returns:
            dict: The dictionary representation of the extension.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["instruction"] = self.instruction.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)

        from lammpsinputbuilder.loader.instruction_loader import InstructionLoader
        loader = InstructionLoader()
        self.instruction = loader.dict_to_instruction(
            d["instruction"], version=version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the extension.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
        """
        return self.instruction.get_do_commands(global_information)

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to remove the extension.

        Instructions don't have undo commands by design, and returns an empty string.

        Returns:
            str: Lammps command(s)
        """
        # Instructions don't have undo commands by design
        return ""


class ManualExtension(Extension):
    """
    A ManualExtension is a way to add manual commands to the workflow
    which will follow the same execution order as the other extensions.
    It should be used for cases where the user needs a command or set of commands
    not currently supported by another extension. In this case, the user is 
    responsible for adding the commands to declare and remove the extension.

    If an Extension is missing from the library, please submit an issue to the Github repository.
    """
    def __init__(
            self,
            extension_name: str = "defaultManualExtension",
            do_cmd: str = "",
            undo_cmd: str = "") -> None:
        """
        Constructor
        Args:
            extension_name (str): The name of the extension. The name must be alpha numeric
                                and start with a letter
            do_cmd (str): The command to execute when the extension is added
            undo_cmd (str): The command to execute when the extension is removed
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(extension_name=extension_name)
        self.do_cmd = do_cmd
        self.undo_cmd = undo_cmd

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the extension.

        Returns:
            dict: The dictionary representation of the extension.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the extension and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the extension.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.do_cmd = d.get("do_cmd", "")
        self.undo_cmd = d.get("undo_cmd", "")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Get the Lammps commands to declare the extension.
        IMPORTANT: For manual commands, the library CANNOT convert units to the right units.
        The user is responsible for providing the right units when declaring the Extension.

        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        if self.do_cmd.endswith("\n"):
            return self.do_cmd
        return self.do_cmd + "\n"

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to remove the extension.

        Returns:
            str: Lammps command(s)
        """
        if self.undo_cmd.endswith("\n"):
            return self.undo_cmd
        return self.undo_cmd + "\n"
