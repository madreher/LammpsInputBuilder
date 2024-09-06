from lammpsinputbuilder.group import AllGroup, Group
from lammpsinputbuilder.quantities import LammpsUnitSystem, TemperatureQuantity, TimeQuantity, ForceQuantity, VelocityQuantity

class Extension:
    def __init__(self, computationName: str = "defaultComputation") -> None:
        self.computationName = computationName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__ 
        result["computationName"] = self.computationName
        return result

    def fromDict(self, d: dict, version: int):
        self.computationName = d.get("computationName", "defaultComputation")

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    
class LangevinCompute(Extension):
    def __init__(self, 
                 computationName: str = "defaultLangevinCompute", 
                 group: Group = AllGroup(), 
                 startTemp: TemperatureQuantity = TemperatureQuantity(1.0, "K"),
                 endTemp: TemperatureQuantity = TemperatureQuantity(1.0, "K"),
                 damp: TimeQuantity = TimeQuantity(10.0, "ps"),
                 seed: int = 122345) -> None:
        super().__init__(computationName=computationName)
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
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.startTemp = TemperatureQuantity()
        self.startTemp.fromDict(d["startTemp"], version)
        self.endTemp = TemperatureQuantity()
        self.endTemp.fromDict(d["endTemp"], version)
        self.damp = TimeQuantity()
        self.damp.fromDict(d["damp"], version)
        self.seed = d.get("seed", 122345)

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return f"fix {self.computationName} {self.group} langevin {self.startTemp.convertTo(unitsystem)} {self.endTemp.convertTo(unitsystem)} {self.damp.convertTo(unitsystem)} {self.seed}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.computationName}\n"
    
class SetForceCompute(Extension):
    def __init__(self, 
                 computationName: str = "defaultSetForceCompute", 
                 group: Group = AllGroup(),
                 fx: ForceQuantity = ForceQuantity(0.0, "(kcal/mol)/angstrom"),
                 fy: ForceQuantity = ForceQuantity(0.0, "(kcal/mol)/angstrom"),
                 fz: ForceQuantity = ForceQuantity(0.0, "(kcal/mol)/angstrom")) -> None:
        super().__init__(computationName=computationName)
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
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.fx = ForceQuantity()
        self.fx.fromDict(d["fx"], version)
        self.fy = ForceQuantity()
        self.fy.fromDict(d["fy"], version)
        self.fz = ForceQuantity()
        self.fz.fromDict(d["fz"], version)

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return f"fix {self.computationName} {self.group} setforce {self.fx.convertTo(unitsystem)} {self.fy.convertTo(unitsystem)} {self.fz.convertTo(unitsystem)}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.computationName}\n"
    
class MoveCompute(Extension):
    def __init__(self, 
                 computationName: str = "defaultMoveCompute", 
                 group: Group = AllGroup(),
                 vx: VelocityQuantity = VelocityQuantity(0.0, "angstrom/ps"),
                 vy: VelocityQuantity = VelocityQuantity(0.0, "angstrom/ps"),
                 vz: VelocityQuantity = VelocityQuantity(0.0, "angstrom/ps")) -> None:
        super().__init__(computationName=computationName)
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
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version)
        self.group = d.get("group", AllGroup().getGroupName())
        self.vx = VelocityQuantity()
        self.vx.fromDict(d["vx"], version)
        self.vy = VelocityQuantity()
        self.vy.fromDict(d["vy"], version)
        self.vz = VelocityQuantity()
        self.vz.fromDict(d["vz"], version)

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return f"fix {self.computationName} {self.group} move linear {self.vx.convertTo(unitsystem)} {self.vy.convertTo(unitsystem)} {self.vz.convertTo(unitsystem)}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.computationName}\n"