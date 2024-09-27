from enum import Enum

from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.types import GlobalInformation


class Integrator:
    def __init__(self, integratorName: str = "defaultIntegrator") -> None:
        self.integratorName = integratorName

    def getIntegratorName(self) -> str:
        return self.integratorName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["integratorName"] = self.integratorName
        return result

    def fromDict(self, d: dict, version: int):
        self.integratorName = d.get("integratorName", "defaultIntegrator")

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
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
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)

    def addRunCommands(self) -> str:
        return "run 0\n"


class NVEIntegrator(Integrator):
    def __init__(
            self,
            integratorName: str = "NVEID",
            group: Group = AllGroup(),
            nbSteps: int = 5000) -> None:
        super().__init__(integratorName=integratorName)
        self.group = group.getGroupName()
        self.nbSteps = nbSteps

    def getGroupName(self) -> str:
        return self.group

    def getNbSteps(self) -> int:
        return self.nbSteps

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["groupName"] = self.group
        result["nbSteps"] = self.nbSteps
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.group = d["groupName"]
        self.nbSteps = d.get("nbSteps", 5000)

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return f"fix {self.integratorName} {self.group} nve\n"

    def addUndoCommands(self) -> str:
        return f"unfix {self.integratorName}\n"

    def addRunCommands(self) -> str:
        return f"run {self.nbSteps}\n"


class MinimizeStyle(Enum):
    CG = 0,
    SD = 1,
    SPIN_LBFGS = 2


class MinimizeIntegrator(Integrator):

    minimizeStyleToStr = {
        MinimizeStyle.CG: "cg",
        MinimizeStyle.SD: "sd",
        MinimizeStyle.SPIN_LBFGS: "spin/lbfgs"
    }

    def __init__(
            self,
            integratorName: str = "Minimize",
            style: MinimizeStyle = MinimizeStyle.CG,
            etol: float = 0.01,
            ftol: float = 0.01,
            maxiter: int = 100,
            maxeval: int = 10000) -> None:
        super().__init__(integratorName=integratorName)
        self.style = style
        self.etol = etol
        self.ftol = ftol
        self.maxiter = maxiter
        self.maxeval = maxeval

    def getStyle(self) -> MinimizeStyle:
        return self.style

    def getEtol(self) -> float:
        return self.etol

    def getFtol(self) -> float:
        return self.ftol

    def getMaxiter(self) -> int:
        return self.maxiter

    def getMaxeval(self) -> int:
        return self.maxeval

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
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.style = MinimizeStyle(d["style"])
        self.etol = d["etol"]
        self.ftol = d["ftol"]
        self.maxiter = d["maxiter"]
        self.maxeval = d["maxeval"]

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

    def addRunCommands(self) -> str:
        result = f"min_style {MinimizeIntegrator.minimizeStyleToStr[self.style]}\n"
        result += f"minimize {self.etol} {self.ftol} {self.maxiter} {self.maxeval}\n"
        return result

    def getMinimizeStyle(self) -> MinimizeStyle:
        return self.style


class MultipassMinimizeIntegrator(Integrator):

    def __init__(self, integratorName: str = "MultiMinimize") -> None:
        super().__init__(integratorName=integratorName)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

    def addRunCommands(self) -> str:
        commands = ""
        commands += "min_style      cg\n"
        commands += "minimize       1.0e-10 1.0e-10 10000 100000\n"

        commands += "min_style      hftn\n"
        commands += "minimize       1.0e-10 1.0e-10 10000 100000\n"

        commands += 'min_style      sd\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'variable       i loop 100\n'
        commands += 'label          loop1\n'
        commands += 'variable       ene_min equal pe\n'
        commands += 'variable       ene_min_i equal ${ene_min}\n'

        commands += 'min_style      cg\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'min_style      hftn\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'min_style      sd\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'variable       ene_min_f equal pe\n'
        commands += 'variable       ene_diff equal ${ene_min_i}-${ene_min_f}\n'
        commands += 'print          "Delta_E = ${ene_diff}"\n'
        commands += 'if             "${ene_diff}<1e-6" then "jump SELF break1"\n'
        commands += 'print          "Loop_id = $i"\n'
        commands += 'next           i\n'
        commands += 'jump           SELF loop1\n'
        commands += 'label          break1\n'
        commands += 'variable       i delete\n'
        return commands


class ManualIntegrator(Integrator):

    def __init__(
            self,
            integratorName: str = "Manual",
            cmdDo: str = "",
            cmdUndo: str = "",
            cmdRun: str = "") -> None:
        super().__init__(integratorName=integratorName)
        self.cmdDo = cmdDo
        self.cmdUndo = cmdUndo
        self.cmdRun = cmdRun

    def getDoCommands(self) -> str:
        return self.cmdDo

    def getUndoCommands(self) -> str:
        return self.cmdUndo

    def getRunCommands(self) -> str:
        return self.cmdRun

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["cmdDo"] = self.cmdDo
        result["cmdUndo"] = self.cmdUndo
        result["cmdRun"] = self.cmdRun
        return result

    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version)
        self.cmdDo = d["cmdDo"]
        self.cmdUndo = d["cmdUndo"]
        self.cmdRun = d["cmdRun"]

    def addDoCommands(self, globalInformation: GlobalInformation) -> str:
        if self.cmdDo.endswith("\n"):
            return self.cmdDo
        else:
            return self.cmdDo + "\n"

    def addUndoCommands(self) -> str:
        if self.cmdUndo.endswith("\n"):
            return self.cmdUndo
        else:
            return self.cmdUndo + "\n"

    def addRunCommands(self) -> str:
        if self.cmdRun.endswith("\n"):
            return self.cmdRun
        else:
            return self.cmdRun + "\n"
