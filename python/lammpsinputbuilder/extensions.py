from lammpsinputbuilder.group import AllGroup, Group
from lammpsinputbuilder.quantities import LammpsUnitSystem, TemperatureQuantity, TimeQuantity, ForceQuantity, VelocityQuantity
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.instructions import Instruction


class Extension:
    def __init__(self, extensionName: str = "defaultExtension") -> None:
        self.extensionName = extensionName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["extensionName"] = self.extensionName
        return result

    def fromDict(self, d: dict, version: int):
        self.extensionName = d.get("extensionName", "defaultExtension")

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""


class LangevinExtension(Extension):
    def __init__(
            self,
            extensionName: str = "defaultLangevinExtension",
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
        super().__init__(extensionName=extensionName)
        self.group = group.getGroupName()
        self.startTemp = startTemp
        self.endTemp = endTemp
        self.damp = damp
        self.seed = seed

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["startTemp"] = self.startTemp.toDict()
        result["endTemp"] = self.endTemp.toDict()
        result["damp"] = self.damp.toDict()
        result["seed"] = self.seed
        return result

    def fromDict(self, d: dict, version: int):
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.startTemp = TemperatureQuantity()
        self.startTemp.fromDict(d["startTemp"], version)
        self.endTemp = TemperatureQuantity()
        self.endTemp.fromDict(d["endTemp"], version)
        self.damp = TimeQuantity()
        self.damp.fromDict(d["damp"], version)
        self.seed = d.get("seed", 122345)

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return f"fix {self.extensionName} {self.group} langevin {self.startTemp.convertTo(globalInformation.getUnitStyle())} {self.endTemp.convertTo(globalInformation.getUnitStyle())} {self.damp.convertTo(globalInformation.getUnitStyle())} {self.seed}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.extensionName}\n"


class SetForceExtension(Extension):
    def __init__(
        self,
        extensionName: str = "defaultSetForceExtension",
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
        super().__init__(extensionName=extensionName)
        self.group = group.getGroupName()
        self.fx = fx
        self.fy = fy
        self.fz = fz

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["fx"] = self.fx.toDict()
        result["fy"] = self.fy.toDict()
        result["fz"] = self.fz.toDict()
        return result

    def fromDict(self, d: dict, version: int):
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.fx = ForceQuantity()
        self.fx.fromDict(d["fx"], version)
        self.fy = ForceQuantity()
        self.fy.fromDict(d["fy"], version)
        self.fz = ForceQuantity()
        self.fz.fromDict(d["fz"], version)

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return f"fix {self.extensionName} {self.group} setforce {self.fx.convertTo(globalInformation.getUnitStyle())} {self.fy.convertTo(globalInformation.getUnitStyle())} {self.fz.convertTo(globalInformation.getUnitStyle())}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.extensionName}\n"


class MoveExtension(Extension):
    def __init__(
        self,
        extensionName: str = "defaultMoveExtension",
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
        super().__init__(extensionName=extensionName)
        self.group = group.getGroupName()
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["vx"] = self.vx.toDict()
        result["vy"] = self.vy.toDict()
        result["vz"] = self.vz.toDict()
        return result

    def fromDict(self, d: dict, version: int):
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.vx = VelocityQuantity()
        self.vx.fromDict(d["vx"], version)
        self.vy = VelocityQuantity()
        self.vy.fromDict(d["vy"], version)
        self.vz = VelocityQuantity()
        self.vz.fromDict(d["vz"], version)

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return f"fix {self.extensionName} {self.group} move linear {self.vx.convertTo(globalInformation.getUnitStyle())} {self.vy.convertTo(globalInformation.getUnitStyle())} {self.vz.convertTo(globalInformation.getUnitStyle())}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.extensionName}\n"


class InstructionExtension(Extension):
    def __init__(self, instruction: Instruction = Instruction()) -> None:
        super().__init__(instruction.getInstructionName())
        self.instruction = instruction

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["instruction"] = self.instruction.toDict()
        return result

    def fromDict(self, d: dict, version: int):
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)

        from lammpsinputbuilder.loader.instructionLoader import InstructionLoader
        loader = InstructionLoader()
        self.instruction = loader.dictToInstruction(
            d["instruction"], version=version)

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return self.instruction.getDoCommands(globalInformation)

    def addUndoCommands(self) -> str:
        # Instructions don't have undo commands by design
        return ""


class ManualExtension(Extension):
    def __init__(
            self,
            extensionName: str = "defaultManualExtension",
            doCmd: str = "",
            undoCmd: str = "") -> None:
        super().__init__(extensionName=extensionName)
        self.doCmd = doCmd
        self.undoCmd = undoCmd

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["doCmd"] = self.doCmd
        result["undoCmd"] = self.undoCmd
        return result

    def fromDict(self, d: dict, version: int):
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.doCmd = d.get("doCmd", "")
        self.undoCmd = d.get("undoCmd", "")

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        if self.doCmd.endswith("\n"):
            return self.doCmd
        else:
            return self.doCmd + "\n"

    def addUndoCommands(self) -> str:
        if self.undoCmd.endswith("\n"):
            return self.undoCmd
        else:
            return self.undoCmd + "\n"
