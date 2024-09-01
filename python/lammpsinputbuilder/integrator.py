from lammpsinputbuilder.group import Group, AllGroup

from enum import Enum

class Integrator:
    def __init__(self, integratorName: str = "defaultIntegrator") -> None:
        self.integratorName = integratorName

    def getIntegratorName(self) -> str:
        return self.integratorName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["integratorName"] = self.integratorName

    def fromDict(self, d: dict, version: int):
        self.integratorName = d.get("integratorName", "defaultIntegrator")

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    
    def addRunCommands(self) -> str:
        return ""

class RunZeroIntegrator(Integrator):
    def __init__(self, integratorName: str = "RunZero") -> None:
        super().__init__(integratorName=integratorName)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)

    def addRunCommands(self) -> str:
        return f"run 0\n"

class NVEIntegrator(Integrator):
    def __init__(self, integratorName: str = "NVEID", group: Group = AllGroup(), nbSteps: int = 5000) -> None:
        super().__init__(integratorName=integratorName)
        self.group = group.getGroupName()
        self.nbSteps = nbSteps

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["group"] = self.group
        result["nbSteps"] = self.nbSteps
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.group = d["group"]
        self.nbSteps = d["nbSteps"]


    def addDoCommands(self) -> str:
        return f"fix {self.integratorName} {self.group} nve\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.integratorName}\n"
    
    def addRunCommands(self) -> str:
        return f"run {self.nbSteps}\n"
    

class MinimizeStyle(Enum):
    CG = "cg",
    SD = "sd",
    SPIN_LBFGS = "spin/lbfgs"


class MinimizeIntegrator(Integrator):
    def __init__(self, integratorName: str = "Minimize", style: MinimizeStyle = MinimizeStyle.CG, etol: float = 0.01, ftol: float = 0.01, maxiter: int = 100, maxeval: int = 10000) -> None:
        super().__init__(integratorName=integratorName)
        self.style = style
        self.etol = etol
        self.ftol = ftol
        self.maxiter = maxiter
        self.maxeval = maxeval

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["style"] = self.style.value
        result["etol"] = self.etol
        result["ftol"] = self.ftol
        result["maxiter"] = self.maxiter
        result["maxeval"] = self.maxeval
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d)
        self.style = MinimizeStyle(d["style"])
        self.etol = d["etol"]
        self.ftol = d["ftol"]
        self.maxiter = d["maxiter"]
        self.maxeval = d["maxeval"]


    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

    def addRunCommands(self) -> str:
        result = f"min_style {self.style.value}\n"
        result +=f"minimize {self.etol} {self.ftol} {self.maxiter} {self.maxeval}\n"
        return result
    
    def getMinimizeStyle(self) -> MinimizeStyle:
        return self.style