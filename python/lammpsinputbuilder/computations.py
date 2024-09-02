from lammpsinputbuilder.group import AllGroup, Group
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity, ForceQuantity

class Computations:
    def __init__(self, computationName: str = "defaultComputation") -> None:
        self.computationName = computationName

    def toDict(self) -> dict:
        result  = super().toDict()
        result["class"] = self.__class__.__name__ 
        result["computationName"] = self.computationName
        return result

    def fromDict(self, d: dict, version: int):
        self.computationName = d.get("computationName", "defaultComputation")

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    
class LangevinCompute(Computations):
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
        self.startTemp = TemperatureQuantity.fromDict(d["startTemp"])
        self.endTemp = TemperatureQuantity.fromDict(d["endTemp"])
        self.damp = TimeQuantity.fromDict(d["damp"])
        self.seed = d.get("seed", 122345)

    def addDoCommands(self) -> str:
        return f"fix {self.computationName} {self.group} langevin {self.startTemp} {self.endTemp} {self.damp} {self.seed}"

    def addUndoCommands(self) -> str:
        return f"unfix {self.computationName}"
    
class SetForceCompute(Computations):
    def __init__(self, 
                 computationName: str = "defaultSetForceCompute", 
                 group: Group = AllGroup(),
                 fx: ForceQuantity = ForceQuantity(0.0, "(kcal/mol)/Angstrom"),
                 fy: ForceQuantity = ForceQuantity(0.0, "(kcal/mol)/Angstrom"),
                 fz: ForceQuantity = ForceQuantity(0.0, "(kcal/mol)/Angstrom")) -> None:
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
        self.fx = ForceQuantity.fromDict(d["fx"], version)
        self.fy = ForceQuantity.fromDict(d["fy"], version)
        self.fz = ForceQuantity.fromDict(d["fz"], version)

    def addDoCommands(self) -> str:
        return f"fix {self.computationName} {self.group} setforce {self.fx.getValue()} {self.fy.getValue().getValue()} {self.fz.getValue()}\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.computationName}"