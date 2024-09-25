from lammpsinputbuilder.quantities import TimeQuantity, LammpsUnitSystem, TemperatureQuantity
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.quantities import LengthQuantity
from lammpsinputbuilder.types import GlobalInformation

from enum import Enum

class Instruction:
    def __init__(self, instructionName: str = "defaultInstruction") -> None:
        self.instructionName = instructionName

    def getInstructionName(self) -> str:
        return self.instructionName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["instructionName"] = self.instructionName
        return result
    
    def fromDict(self, d: dict, version: int):
        self.instructionName = d.get("instructionName", "defaultInstruction")

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return ""
    
class ResetTimestepInstruction(Instruction):
    def __init__(self, instructionName: str = "defaultResetTimestep", timestep: int = 0) -> None:
        super().__init__(instructionName=instructionName)
        self.timestep = timestep
        self.validate()

    def validate(self):
        if self.timestep < 0:
            raise ValueError(f"Invalid timestep {self.timestep} in Intruction {self.instructionName}.")
        
    def getTimestep(self) -> int:
        return self.timestep

    def toDict(self) -> dict:
        result = super().toDict()
        result["timestep"] = self.timestep
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.timestep = d.get("timestep", 0)
        self.validate()

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return f"reset_timestep {self.timestep}\n"
    
class SetTimestepInstruction(Instruction):
    def __init__(self, instructionName: str = "defaultTimeStep", timestep: TimeQuantity = TimeQuantity(1, "fs")) -> None:
        super().__init__(instructionName=instructionName)
        self.timestep = timestep
        self.validate()

    def getTimestep(self) -> TimeQuantity:
        return self.timestep

    def validate(self):
        if self.timestep.getMagnitude() < 0:
            raise ValueError(f"Invalid timestep {self.timestep.getMagnitude()} in Intruction {self.instructionName}.")
        
    def toDict(self) -> dict:
        result = super().toDict()
        result["timestep"] = self.timestep.toDict()
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.timestep = TimeQuantity()
        self.timestep.fromDict(d["timestep"], version)
        self.validate()

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return f"timestep {self.timestep.convertTo(globalInformation.getUnitStyle())}\n"
    
class VelocityCreateInstruction(Instruction):
    def __init__(self, instructionName: str = "defaultVelocityCreate", group: Group = AllGroup(), temp: TemperatureQuantity = TemperatureQuantity(300, "kelvin"), seed: int =12335) -> None:
        super().__init__(instructionName=instructionName)
        self.group = group.getGroupName()
        self.temp = temp
        self.seed = seed
        self.validate()

    def getGroupName(self) -> str:
        return self.group
    
    def getTemp(self) -> TemperatureQuantity:
        return self.temp
    
    def getSeed(self) -> int:
        return self.seed

    def validate(self):
        if self.temp.getMagnitude() < 0:
            raise ValueError(f"Invalid temperature {self.temp.getMagnitude()} in Intruction {self.instructionName}.")

    def toDict(self) -> dict:
        result = super().toDict()
        result["groupName"] = self.group
        result["temp"] = self.temp.toDict()
        result["seed"] = self.seed
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.group = d.get("groupName", AllGroup().getGroupName())
        self.temp = TemperatureQuantity()
        self.temp.fromDict(d["temp"], version)
        self.seed = d.get("seed", 12335)
        self.validate()

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return f"velocity {self.group} create {self.temp.convertTo(globalInformation.getUnitStyle())} {self.seed} dist gaussian\n"
    

class VariableStyle(Enum):
    DELETE = 0, 
    ATOMFILE = 1, 
    FILE = 2, 
    FORMAT = 3,
    GETENV = 4,
    INDEX = 5,
    INTERNAL = 6,
    LOOP = 7,
    PYTHON = 8,
    STRING = 9,
    TIMER = 10,
    ULOOP = 11,
    UNIVERSE = 12,
    WORLD = 13,
    EQUAL = 14,
    VECTOR = 15,
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

    def __init__(self, instructionName: str = "defaultVariable", variableName: str = "defaultVariable", style: VariableStyle = VariableStyle.EQUAL, args: str = "") -> None:
        super().__init__(instructionName=instructionName)
        self.variableName = variableName
        self.style = style
        self.args = args
        self.validate()

    def getVariableName(self) -> str:
        return self.variableName
    
    def getVariableStyle(self) -> VariableStyle:
        return self.style
    
    def getArgs(self) -> str:
        return self.args

    def validate(self):
        pass 

    def toDict(self) -> dict:
        result = super().toDict()
        result["variableName"] = self.variableName
        result["style"] = self.style.value
        result["args"] = self.args
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.variableName = d.get("variableName", "defaultVariable")
        self.style = VariableStyle(d.get("style", VariableStyle.EQUAL.value))
        self.args = d.get("args", "")
        self.validate()

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return f"variable {self.variableName} {self.variableStyleToStr[self.style]} {self.args}\n"

class DisplaceAtomsInstruction(Instruction):
    def __init__(self, instructionName: str = "defaultDisplaceAtoms", group: Group = AllGroup(), dx: LengthQuantity = LengthQuantity(0.0, "lmp_real_length"), dy: LengthQuantity = LengthQuantity(0.0, "lmp_real_length"), dz: LengthQuantity = LengthQuantity(0.0, "lmp_real_length")) -> None:
        """
        Initializes a new instance of the DisplaceAtomsInstruction class.

        Parameters:
        instructionName (str): The name of the instruction. Defaults to "defaultDisplaceAtom".
        group (Group): The group to which the instruction belongs. Defaults to AllGroup.
        dx (LengthQuantity): The displacement in the x-direction. Defaults to LengthQuantity(0.0, "lmp_real_length").
        dy (LengthQuantity): The displacement in the y-direction. Defaults to LengthQuantity(0.0, "lmp_real_length").
        dz (LengthQuantity): The displacement in the z-direction. Defaults to LengthQuantity(0.0, "lmp_real_length").

        Returns:
        None
        """
        super().__init__(instructionName=instructionName)
        self.group = group.getGroupName()
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.validate()

    def validate(self) -> bool:
        return True
    
    def getGroupName(self) -> str:
        return self.group
    
    def getDisplacement(self) -> tuple[LengthQuantity, LengthQuantity, LengthQuantity]:
        return self.dx, self.dy, self.dz

    def toDict(self) -> dict:
        result = super().toDict()
        result["group"] = self.group
        result["dx"] = self.dx.toDict()
        result["dy"] = self.dy.toDict()
        result["dz"] = self.dz.toDict()
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.dx = LengthQuantity()
        self.dx.fromDict(d.get("dx", {}))
        self.dy = LengthQuantity()
        self.dy.fromDict(d.get("dy", {}))
        self.dz = LengthQuantity()
        self.dz.fromDict(d.get("dz", {}))
        self.validate()

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return f"displace_atoms {self.group} move {self.dx.convertTo(globalInformation.getUnitStyle())} {self.dy.convertTo(globalInformation.getUnitStyle())} {self.dz.convertTo(globalInformation.getUnitStyle())}\n"

class ManualInstruction(Instruction):
    def __init__(self, instructionName: str = "defaultManual", cmd: str = "") -> None:
        super().__init__(instructionName=instructionName)
        self.cmd = cmd

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["cmd"] = self.cmd
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.cmd = d.get("cmd", "")

    def writeInstruction(self, globalInformation:GlobalInformation) -> str:
        return f"{self.cmd}\n"