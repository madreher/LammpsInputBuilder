"""Module containing the definition of the Instruction class and its subclasses."""

from enum import Enum

from lammpsinputbuilder.quantities import TimeQuantity, TemperatureQuantity
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.quantities import LengthQuantity
from lammpsinputbuilder.types import GlobalInformation


class Instruction:
    def __init__(self, instruction_name: str = "defaultInstruction") -> None:
        self.instruction_name = instruction_name

    def getInstructionName(self) -> str:
        return self.instruction_name

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["instruction_name"] = self.instruction_name
        return result

    def from_dict(self, d: dict, version: int):
        self.instruction_name = d.get("instruction_name", "defaultInstruction")

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return ""


class ResetTimestepInstruction(Instruction):
    def __init__(
            self,
            instruction_name: str = "defaultResetTimestep",
            timestep: int = 0) -> None:
        super().__init__(instruction_name=instruction_name)
        self.timestep = timestep
        self.validate()

    def validate(self):
        if self.timestep < 0:
            raise ValueError(
                f"Invalid timestep {self.timestep} in Intruction {self.instruction_name}.")

    def get_timestep(self) -> int:
        return self.timestep

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["timestep"] = self.timestep
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version)
        self.timestep = d.get("timestep", 0)
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return f"reset_timestep {self.timestep}\n"


class SetTimestepInstruction(Instruction):
    def __init__(
        self,
        instruction_name: str = "defaultTimeStep",
        timestep: TimeQuantity = TimeQuantity(
            1,
            "fs")) -> None:
        super().__init__(instruction_name=instruction_name)
        self.timestep = timestep
        self.validate()

    def get_timestep(self) -> TimeQuantity:
        return self.timestep

    def validate(self):
        if self.timestep.getMagnitude() < 0:
            raise ValueError(
                f"Invalid timestep {self.timestep.getMagnitude()} in Intruction {self.instruction_name}.")

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["timestep"] = self.timestep.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version)
        self.timestep = TimeQuantity()
        self.timestep.from_dict(d["timestep"], version)
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return f"timestep {self.timestep.convertTo(global_information.getUnitStyle())}\n"


class VelocityCreateInstruction(Instruction):
    def __init__(
            self,
            instruction_name: str = "defaultVelocityCreate",
            group: Group = AllGroup(),
            temp: TemperatureQuantity = TemperatureQuantity(
                300,
                "kelvin"),
            seed: int = 12335) -> None:
        super().__init__(instruction_name=instruction_name)
        self.group = group.get_group_name()
        self.temp = temp
        self.seed = seed
        self.validate()

    def get_group_name(self) -> str:
        return self.group

    def get_temp(self) -> TemperatureQuantity:
        return self.temp

    def get_seed(self) -> int:
        return self.seed

    def validate(self):
        if self.temp.getMagnitude() < 0:
            raise ValueError(
                f"Invalid temperature {self.temp.getMagnitude()} in Intruction {self.instruction_name}.")

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["group_name"] = self.group
        result["temp"] = self.temp.to_dict()
        result["seed"] = self.seed
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version)
        self.group = d.get("group_name", AllGroup().get_group_name())
        self.temp = TemperatureQuantity()
        self.temp.from_dict(d["temp"], version)
        self.seed = d.get("seed", 12335)
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return f"velocity {self.group} create {self.temp.convertTo(global_information.getUnitStyle())} {self.seed} dist gaussian\n"


class VariableStyle(Enum):
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
        super().__init__(instruction_name=instruction_name)
        self.variable_name = variable_name
        self.style = style
        self.args = args
        self.validate()

    def get_variable_name(self) -> str:
        return self.variable_name

    def get_variable_style(self) -> VariableStyle:
        return self.style

    def get_args(self) -> str:
        return self.args

    def validate(self):
        pass

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["variable_name"] = self.variable_name
        result["style"] = self.style.value
        result["args"] = self.args
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version)
        self.variable_name = d.get("variable_name", "defaultVariable")
        self.style = VariableStyle(d.get("style", VariableStyle.EQUAL.value))
        self.args = d.get("args", "")
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return f"variable {self.variable_name} {self.variableStyleToStr[self.style]} {self.args}\n"


class DisplaceAtomsInstruction(Instruction):
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
        Initializes a new instance of the DisplaceAtomsInstruction class.

        Parameters:
        instruction_name (str): The name of the instruction. Defaults to "defaultDisplaceAtom".
        group (Group): The group to which the instruction belongs. Defaults to AllGroup.
        dx (LengthQuantity): The displacement in the x-direction. Defaults to LengthQuantity(0.0, "lmp_real_length").
        dy (LengthQuantity): The displacement in the y-direction. Defaults to LengthQuantity(0.0, "lmp_real_length").
        dz (LengthQuantity): The displacement in the z-direction. Defaults to LengthQuantity(0.0, "lmp_real_length").

        Returns:
        None
        """
        super().__init__(instruction_name=instruction_name)
        self.group = group.get_group_name()
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.validate()

    def validate(self) -> bool:
        return True

    def get_group_name(self) -> str:
        return self.group

    def get_displacement(
            self) -> tuple[LengthQuantity, LengthQuantity, LengthQuantity]:
        return self.dx, self.dy, self.dz

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["group"] = self.group
        result["dx"] = self.dx.to_dict()
        result["dy"] = self.dy.to_dict()
        result["dz"] = self.dz.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version)
        self.group = d.get("group", AllGroup().get_group_name())
        self.dx = LengthQuantity()
        self.dx.from_dict(d.get("dx", {}))
        self.dy = LengthQuantity()
        self.dy.from_dict(d.get("dy", {}))
        self.dz = LengthQuantity()
        self.dz.from_dict(d.get("dz", {}))
        self.validate()

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return f"displace_atoms {self.group} move {self.dx.convertTo(global_information.getUnitStyle())} {self.dy.convertTo(global_information.getUnitStyle())} {self.dz.convertTo(global_information.getUnitStyle())}\n"


class ManualInstruction(Instruction):
    def __init__(
            self,
            instruction_name: str = "defaultManual",
            cmd: str = "") -> None:
        super().__init__(instruction_name=instruction_name)
        self.cmd = cmd

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["cmd"] = self.cmd
        return result

    def from_dict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version)
        self.cmd = d.get("cmd", "")

    def write_instruction(self, global_information: GlobalInformation) -> str:
        return f"{self.cmd}\n"
