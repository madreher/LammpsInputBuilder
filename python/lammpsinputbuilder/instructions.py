"""Module containing the definition of the Instruction class and its subclasses."""

from enum import IntEnum

from lammpsinputbuilder.quantities import TimeQuantity, TemperatureQuantity
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.quantities import LengthQuantity
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.base import BaseObject

class Instruction(BaseObject):
    """
    Base class for all the instructions. An Instruction represents a command or series of commands
    which do not have a scope. An Instruction performs a one time operation outside of time integration
    sections.
    """
    def __init__(self, instruction_name: str = "defaultInstruction") -> None:
        """
        Constructor for the Instruction class.
        Args:
            instruction_name (str): The name of the instruction. The name must be alpha numeric
                                    and start with a letter
        Returns:
            None
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(id_name=instruction_name)

    def get_instruction_name(self) -> str:
        """
        Returns the name of the instruction
        
        Returns:
            str: The name of the instruction
        """
        return super().get_id_name()

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction
        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Generate the command(s) to execute the instruction.
        Args:
            global_information (GlobalInformation): The global information to use
        Returns:
            str: The command(s) to execute the instruction
        Raise:
            NotImplementedError: If the instruction is not implemented by the subclass
        """
        del global_information  # unused
        raise NotImplementedError(
            f"Write instruction {self.get_instruction_name()} not implemented.")


class ResetTimestepInstruction(Instruction):
    """
    Instruction to reset the timestep.

    Lammps documentation: https://docs.lammps.org/reset_timestep.html
    """
    def __init__(
            self,
            instruction_name: str = "defaultResetTimestep",
            new_timestep: int = 0) -> None:
        """
        Initializes a new instance of the ResetTimestepInstruction class.

        Args:
            instruction_name (str): The name of the instruction. Defaults to "defaultResetTimestep".
            new_timestep (int): The new timestep. Defaults to 0.

        Returns:
            None

        Raise:
            ValueError: If the new timestep is negative
        """
        super().__init__(instruction_name=instruction_name)
        self.new_timestep = new_timestep
        self.validate()

    def validate(self):
        """
        Validate the configuration of the instruction

        Returns:
            None

        Raise:
            ValueError: If the new timestep is negative
        """
        if self.new_timestep < 0:
            raise ValueError(
                f"Invalid timestep {self.new_timestep} in Intruction {self.get_instruction_name()}.")

    def get_new_timestep(self) -> int:
        """
        Returns the new timestep

        Returns:
            int: The new timestep
        """
        return self.new_timestep

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction

        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["new_timestep"] = self.new_timestep
        return result

    def from_dict(self, d: dict, version: int):
        """
        Initializes the instruction from a dictionary

        Args:
            d (dict): The dictionary representation of the instruction
            version (int): The version of the instruction

        Returns:
            None

        Raise:
            ValueError: If the class name in the dictionary doesn't match the class name of the instruction
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.new_timestep = d.get("new_timestep", 0)
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Generate the command(s) to execute the instruction

        Args:
            global_information (GlobalInformation): The global information to use

        Returns:
            str: The command(s) to execute the instruction
        """
        del global_information  # unused
        return f"reset_timestep {self.new_timestep}\n"


class SetTimestepInstruction(Instruction):
    """
    Instruction to set the timestep, ie the time integration step.

    Lammps documentation: https://docs.lammps.org/timestep.html
    """
    def __init__(
        self,
        instruction_name: str = "defaultTimeStep",
        timestep: TimeQuantity = TimeQuantity(
            1,
            "fs")) -> None:
        """
        Initializes a new instance of the SetTimestepInstruction class.

        Args:
            instruction_name (str): The name of the instruction. Defaults to "defaultTimeStep".
            timestep (TimeQuantity): The timestep. Defaults to TimeQuantity(1, "fs").

        Returns:
            None

        Raise:
            ValueError: If the timestep is negative
        """
        super().__init__(instruction_name=instruction_name)
        self.timestep = timestep
        self.validate()

    def get_timestep(self) -> TimeQuantity:
        """
        Returns the timestep

        Returns:
            TimeQuantity: The timestep
        """
        return self.timestep

    def validate(self):
        """
        Validate the configuration of the instruction

        Returns:
            None

        Raise:
            ValueError: If the timestep is negative
        """
        if self.timestep.get_magnitude() < 0:
            raise ValueError(
                (f"Invalid timestep {self.timestep.get_magnitude()} "
                 f"in Intruction {self.get_instruction_name()}."))

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction

        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["timestep"] = self.timestep.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        """
        Initializes the instruction from a dictionary

        Args:
            d (dict): The dictionary representation of the instruction
            version (int): The version of the instruction

        Returns:
            None

        Raise:
            ValueError: If the class name in the dictionary doesn't match the class name of the instruction
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.timestep = TimeQuantity()
        self.timestep.from_dict(d["timestep"], version)
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Generate the command(s) to execute the instruction

        Args:
            global_information (GlobalInformation): The global information to use

        Returns:
            str: The command(s) to execute the instruction
        """
        return f"timestep {self.timestep.convert_to(global_information.get_unit_style())}\n"


class VelocityCreateInstruction(Instruction):
    """
    Instruction to create velocities for a group of atoms.

    Note: This Instruction only supports the "create" style of the "velocity" command.
    For other styles, please use the ManualInstruction instead.

    Lammps documentation: https://docs.lammps.org/velocity.html
    """
    def __init__(
            self,
            instruction_name: str = "defaultVelocityCreate",
            group: Group = AllGroup(),
            temp: TemperatureQuantity = TemperatureQuantity(
                300,
                "kelvin"),
            seed: int = 12335) -> None:
        """
        Initializes a new instance of the VelocityCreateInstruction class.

        Args:
            instruction_name (str): The name of the instruction. Defaults to "defaultVelocityCreate".
            group (Group): The group of atoms. Defaults to AllGroup().
            temp (TemperatureQuantity): The temperature. Defaults to TemperatureQuantity(300, "kelvin").
            seed (int): The seed for the random number generator. Defaults to 12335.

        Returns:
            None
        """
        super().__init__(instruction_name=instruction_name)
        self.group = group.get_group_name()
        self.temp = temp
        self.seed = seed
        self.validate()

    def get_group_name(self) -> str:
        """
        Returns the group name

        Returns:
            str: The group name
        """
        return self.group

    def get_temp(self) -> TemperatureQuantity:
        """
        Returns the temperature used to generate the velocity vectors

        Returns:
            TemperatureQuantity: The temperature
        """
        return self.temp

    def get_seed(self) -> int:
        """
        Returns the seed for the random number generator

        Returns:
            int: The seed for the random number generator
        """
        return self.seed

    def validate(self):
        """
        Validate the configuration of the instruction

        Returns:
            None

        Raise:
            ValueError: If the temperature is negative
        """
        if self.temp.get_magnitude() < 0:
            raise ValueError(
                (f"Invalid temperature {self.temp.get_magnitude()} "
                 f"in Intruction {self.get_instruction_name()}."))

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction

        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["group_name"] = self.group
        result["temp"] = self.temp.to_dict()
        result["seed"] = self.seed
        return result

    def from_dict(self, d: dict, version: int):
        """
        Initializes the instruction from a dictionary

        Args:
            d (dict): The dictionary representation of the instruction
            version (int): The version of the instruction

        Returns:
            None

        Raise:
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.group = d.get("group_name", AllGroup().get_group_name())
        self.temp = TemperatureQuantity()
        self.temp.from_dict(d["temp"], version)
        self.seed = d.get("seed", 12335)
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Generate the command(s) to execute the instruction

        Args:
            global_information (GlobalInformation): The global information to use

        Returns:
            str: The command(s) to execute the instruction
        """
        return (f"velocity {self.group} create "
                f"{self.temp.convert_to(global_information.get_unit_style())} "
                f"{self.seed} dist gaussian\n")


class VariableStyle(IntEnum):
    DELETE = 0
    ATOMFILE = 1
    FILE = 2
    FORMAT = 3
    GETENV = 4
    INDEX = 5
    INTERNAL = 6
    LOOP = 7
    PYTHON = 8
    STRING = 9
    TIMER = 10
    ULOOP = 11
    UNIVERSE = 12
    WORLD = 13
    EQUAL = 14
    VECTOR = 15
    ATOM = 16


class VariableInstruction(Instruction):
    """
    A VariableInstruction is a wrapper around a variable to be used by other instructions or extensions.

    Lammps documentation: https://docs.lammps.org/variable.html
    """
    variableStyleToStr = {
        VariableStyle.DELETE: "delete",
        VariableStyle.ATOMFILE: "atomfile",
        VariableStyle.FILE: "file",
        VariableStyle.FORMAT: "format",
        VariableStyle.GETENV: "getenv",
        VariableStyle.INDEX: "index",
        VariableStyle.INTERNAL: "internal",
        VariableStyle.LOOP: "loop",
        VariableStyle.PYTHON: "python",
        VariableStyle.STRING: "string",
        VariableStyle.TIMER: "timer",
        VariableStyle.ULOOP: "uloop",
        VariableStyle.UNIVERSE: "universe",
        VariableStyle.WORLD: "world",
        VariableStyle.EQUAL: "equal",
        VariableStyle.VECTOR: "vector",
        VariableStyle.ATOM: "atom"
    }

    def __init__(
            self,
            instruction_name: str = "defaultVariable",
            variable_name: str = "defaultVariable",
            style: VariableStyle = VariableStyle.EQUAL,
            args: str = "") -> None:
        """
        Constructor
        Args:
            instruction_name (str, optional): The name of the instruction. Defaults to "defaultVariable".
            variable_name (str, optional): The name of the variable. Defaults to "defaultVariable".
            style (VariableStyle, optional): The style of the variable. Defaults to VariableStyle.EQUAL.
            args (str, optional): The arguments of the variable. Defaults to "".

        """

        super().__init__(instruction_name=instruction_name)
        self.variable_name = variable_name
        self.style = style
        self.args = args
        self.validate()

    def get_variable_name(self) -> str:
        """
        Returns the name of the variable

        Returns:
            str: The name of the variable
        """
        return self.variable_name

    def get_variable_style(self) -> VariableStyle:
        """
        Returns the style of the variable

        Returns:
            VariableStyle: The style of the variable
        """
        return self.style

    def get_args(self) -> str:
        """
        Returns the arguments of the variable

        Returns:
            str: The arguments of the variable
        """
        return self.args

    def validate(self):
        """
        Validate the instruction. Nothing to do here
        """
        pass

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction

        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["variable_name"] = self.variable_name
        result["style"] = self.style.value
        result["args"] = self.args
        return result

    def from_dict(self, d: dict, version: int):
        """
        Create the instruction from the dictionary representation

        Args:
            d (dict): The dictionary representation of the instruction
            version (int): The version of the instruction

        Raises:
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.variable_name = d.get("variable_name", "defaultVariable")
        self.style = VariableStyle(d.get("style", VariableStyle.EQUAL.value))
        self.args = d.get("args", "")
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Write the instruction to a string

        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: The command(s) to execute the instruction
        """
        del global_information  # unused
        return f"variable {self.variable_name} {self.variableStyleToStr[self.style]} {self.args}\n"


class DisplaceAtomsInstruction(Instruction):
    """
    A DisplaceAtomsInstruction translate a group of atom by a given displacement vector.

    Note: The DisplaceAtomsInstruction is currently only supporting the move style of displace_atoms.
    For other styles, please use the ManualInstruction instead.

    Lammps documentation: https://docs.lammps.org/displace_atoms.html
    """
    def __init__(
        self,
        instruction_name: str = "defaultDisplaceAtoms",
        group: Group = AllGroup(),
        dx: LengthQuantity = LengthQuantity(
            0.0,
            "lmp_real_length"),
        dy: LengthQuantity = LengthQuantity(
            0.0,
            "lmp_real_length"),
        dz: LengthQuantity = LengthQuantity(
            0.0,
            "lmp_real_length")) -> None:
        """
        Constructor
        Args:
            instruction_name (str, optional): The name of the instruction. Defaults to "defaultDisplaceAtoms".
            group (Group, optional): The group to apply the instruction to. Defaults to AllGroup().
            dx (LengthQuantity, optional): The x displacement. Defaults to LengthQuantity(0.0, "lmp_real_length").
            dy (LengthQuantity, optional): The y displacement. Defaults to LengthQuantity(0.0, "lmp_real_length").
            dz (LengthQuantity, optional): The z displacement. Defaults to LengthQuantity(0.0, "lmp_real_length").
        """
        super().__init__(instruction_name=instruction_name)
        self.group = group.get_group_name()
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.validate()

    def validate(self) -> bool:
        """
        Validate the instruction. Nothing to do here
        """
        return True

    def get_group_name(self) -> str:
        """
        Returns the name of the group

        Returns:
            str: The name of the group
        """
        return self.group

    def get_displacement(
            self) -> tuple[LengthQuantity, LengthQuantity, LengthQuantity]:
        """
        Returns the displacement vector applied to the group of atoms

        Returns:
            tuple[LengthQuantity, LengthQuantity, LengthQuantity]: The displacement
        """
        return self.dx, self.dy, self.dz

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction

        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["group_name"] = self.group
        result["dx"] = self.dx.to_dict()
        result["dy"] = self.dy.to_dict()
        result["dz"] = self.dz.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        """
        Create the instruction from the dictionary representation

        Args:
            d (dict): The dictionary representation of the instruction
            version (int): The version of the instruction

        Raises:
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.group = d.get("group_name", AllGroup().get_group_name())
        self.dx = LengthQuantity(0.0,"lmp_real_length")
        if "dx" in d:
            self.dx.from_dict(d.get("dx", {}), version=version)

        self.dy = LengthQuantity(0.0,"lmp_real_length")
        if "dy" in d:
            self.dy.from_dict(d.get("dy", {}), version=version)

        self.dz = LengthQuantity(0.0,"lmp_real_length")
        if "dz" in d:
            self.dz.from_dict(d.get("dz", {}), version=version)

        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Write the instruction to a string

        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: The command(s) to execute the instruction
        """
        return (f"displace_atoms {self.group} move "
                f"{self.dx.convert_to(global_information.get_unit_style())} "
                f"{self.dy.convert_to(global_information.get_unit_style())} "
                f"{self.dz.convert_to(global_information.get_unit_style())}\n")


class ManualInstruction(Instruction):
    """
    A ManualInstruction is a way to add manual commands to the workflow
    which will follow the same execution order as the other instructions.
    It should be used for cases where the user needs a command or set of commands
    not currently supported by another instruction. In this case, the user is 
    responsible for adding the commands to declare the necessary instructions.

    If an Instruction is missing from the library, please submit an issue to the Github repository.
    """
    def __init__(
            self,
            instruction_name: str = "defaultManual",
            cmd: str = "") -> None:
        """
        Constructor
        Args:
            instruction_name (str, optional): The name of the instruction. Defaults to "defaultManual".
            cmd (str, optional): The command to execute. Defaults to "".
        """
        super().__init__(instruction_name=instruction_name)
        self.cmd = cmd

    def get_cmd(self) -> str:
        """
        Returns the command to execute

        Returns:
            str: Lammps user command(s)
        """
        return self.cmd

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the instruction

        Returns:
            dict: The dictionary representation of the instruction
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["cmd"] = self.cmd
        return result

    def from_dict(self, d: dict, version: int):
        """
        Create the instruction from the dictionary representation

        Args:
            d (dict): The dictionary representation of the instruction
            version (int): The version of the instruction

        Raises:
            ValueError: If the class_name key is not found or doesn't match the class name
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.cmd = d.get("cmd", "")

    def write_instruction(self, global_information: GlobalInformation) -> str:
        """
        Write the instruction to a string

        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: The command(s) to execute the instruction
        """
        del global_information  # unused
        return f"{self.cmd}\n"
