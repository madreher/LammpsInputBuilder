from lammpsinputbuilder.group import Group, AllGroup

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
        super().fromDict(d)

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
        super().fromDict(d)
        self.group = d["group"]
        self.nbSteps = d["nbSteps"]


    def addDoCommands(self) -> str:
        return f"fix {self.integratorName} {self.group} nve\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.integratorName}\n"
    
    def addRunCommands(self) -> str:
        return f"run {self.nbSteps}\n"