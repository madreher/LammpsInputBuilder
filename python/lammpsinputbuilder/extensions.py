"""Module containing the definition of the Extension class and its subclasses."""

from lammpsinputbuilder.group import AllGroup, Group
from lammpsinputbuilder.quantities import LammpsUnitSystem, TemperatureQuantity, TimeQuantity, ForceQuantity, VelocityQuantity
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.instructions import Instruction


class Extension:
    def __init__(self, extension_name: str = "defaultExtension") -> None:
        self.extension_name = extension_name

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["extension_name"] = self.extension_name
        return result

    def from_dict(self, d: dict, version: int):
        self.extension_name = d.get("extension_name", "defaultExtension")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class LangevinExtension(Extension):
    def __init__(
            self,
            extension_name: str = "defaultLangevinExtension",
            group: Group = AllGroup(),
            startTemp: TemperatureQuantity = TemperatureQuantity(
                1.0,
                "K"),
            endTemp: TemperatureQuantity = TemperatureQuantity(
                1.0,
                "K"),
        damp: TimeQuantity = TimeQuantity(
                10.0,
                "ps"),
            seed: int = 122345) -> None:
        super().__init__(extension_name=extension_name)
        self.group = group.get_group_name()
        self.startTemp = startTemp
        self.endTemp = endTemp
        self.damp = damp
        self.seed = seed

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["startTemp"] = self.startTemp.to_dict()
        result["endTemp"] = self.endTemp.to_dict()
        result["damp"] = self.damp.to_dict()
        result["seed"] = self.seed
        return result

    def from_dict(self, d: dict, version: int):
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.group = d.get("group", AllGroup().get_group_name())
        self.startTemp = TemperatureQuantity()
        self.startTemp.from_dict(d["startTemp"], version)
        self.endTemp = TemperatureQuantity()
        self.endTemp.from_dict(d["endTemp"], version)
        self.damp = TimeQuantity()
        self.damp.from_dict(d["damp"], version)
        self.seed = d.get("seed", 122345)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return f"fix {self.extension_name} {self.group} langevin {self.startTemp.convertTo(global_information.get_unit_style())} {self.endTemp.convertTo(global_information.get_unit_style())} {self.damp.convertTo(global_information.get_unit_style())} {self.seed}\n"

    def add_undo_commands(self) -> str:
        return f"unfix {self.extension_name}\n"


class SetForceExtension(Extension):
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
        super().__init__(extension_name=extension_name)
        self.group = group.get_group_name()
        self.fx = fx
        self.fy = fy
        self.fz = fz

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["fx"] = self.fx.to_dict()
        result["fy"] = self.fy.to_dict()
        result["fz"] = self.fz.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.group = d.get("group", AllGroup().get_group_name())
        self.fx = ForceQuantity()
        self.fx.from_dict(d["fx"], version)
        self.fy = ForceQuantity()
        self.fy.from_dict(d["fy"], version)
        self.fz = ForceQuantity()
        self.fz.from_dict(d["fz"], version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return f"fix {self.extension_name} {self.group} setforce {self.fx.convertTo(global_information.get_unit_style())} {self.fy.convertTo(global_information.get_unit_style())} {self.fz.convertTo(global_information.get_unit_style())}\n"

    def add_undo_commands(self) -> str:
        return f"unfix {self.extension_name}\n"


class MoveExtension(Extension):
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
        super().__init__(extension_name=extension_name)
        self.group = group.get_group_name()
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["vx"] = self.vx.to_dict()
        result["vy"] = self.vy.to_dict()
        result["vz"] = self.vz.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.group = d.get("group", AllGroup().get_group_name())
        self.vx = VelocityQuantity()
        self.vx.from_dict(d["vx"], version)
        self.vy = VelocityQuantity()
        self.vy.from_dict(d["vy"], version)
        self.vz = VelocityQuantity()
        self.vz.from_dict(d["vz"], version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return f"fix {self.extension_name} {self.group} move linear {self.vx.convertTo(global_information.get_unit_style())} {self.vy.convertTo(global_information.get_unit_style())} {self.vz.convertTo(global_information.get_unit_style())}\n"

    def add_undo_commands(self) -> str:
        return f"unfix {self.extension_name}\n"


class InstructionExtension(Extension):
    def __init__(self, instruction: Instruction = Instruction()) -> None:
        super().__init__(instruction.getInstructionName())
        self.instruction = instruction

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["instruction"] = self.instruction.to_dict()
        return result

    def from_dict(self, d: dict, version: int):
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)

        from lammpsinputbuilder.loader.instructionLoader import InstructionLoader
        loader = InstructionLoader()
        self.instruction = loader.dict_to_instruction(
            d["instruction"], version=version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return self.instruction.getDoCommands(global_information)

    def add_undo_commands(self) -> str:
        # Instructions don't have undo commands by design
        return ""


class ManualExtension(Extension):
    def __init__(
            self,
            extension_name: str = "defaultManualExtension",
            do_cmd: str = "",
            undo_cmd: str = "") -> None:
        super().__init__(extension_name=extension_name)
        self.do_cmd = do_cmd
        self.undo_cmd = undo_cmd

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        return result

    def from_dict(self, d: dict, version: int):
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version)
        self.do_cmd = d.get("do_cmd", "")
        self.undo_cmd = d.get("undo_cmd", "")

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        if self.do_cmd.endswith("\n"):
            return self.do_cmd
        else:
            return self.do_cmd + "\n"

    def add_undo_commands(self) -> str:
        if self.undo_cmd.endswith("\n"):
            return self.undo_cmd
        else:
            return self.undo_cmd + "\n"
