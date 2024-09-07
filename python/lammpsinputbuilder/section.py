from typing import List

from lammpsinputbuilder.integrator import Integrator, RunZeroIntegrator
from lammpsinputbuilder.fileIO import FileIO
from lammpsinputbuilder.quantities import LammpsUnitSystem
from lammpsinputbuilder.instructions import Instruction

class Section:
    def __init__(self, sectionName: str = "defaultSection") -> None:
        self.sectionName = sectionName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["sectionName"] = self.sectionName
        return result

    def fromDict(self, d: dict):
        self.sectionName = d.get("sectionName", "defaultSection")
        return
    
    def addAllCommands(self) -> str:
        result = ""
        result += self.addDoCommands()
        result += self.addUndoCommands()
        return result
    
    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return ""
    
    def addUndoCommands(self) -> str:
        return ""
    


class RecusiveSection(Section):
    def __init__(self) -> None:
        super().__init__()
        self.sections: List[Section] = []

    def addSection(self, section: Section):
        self.sections.append(section)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["sections"] = [s.toDict() for s in self.sections]
        return result
    
    def fromDict(self, d: dict, version: int):
        super().fromDict(d, version=version)
        self.sections = [Section.fromDict(s) for s in d["sections"]]

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return ""
    
    def addUndoCommands(self) -> str:
        return ""

class IntegratorSection(Section):
    def __init__(self, integrator: Integrator = RunZeroIntegrator()) -> None:
        super().__init__()
        self.integrator = integrator
        self.fileIOs = []

    def addFileIO(self, fileIO: FileIO):
        self.fileIOs.append(fileIO)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["integrator"] = self.integrator.toDict()
        return result
    
    def fromDict(self, d: dict, version: int):
        super().fromDict(d, version=version)
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        if "integrator" not in d.keys():
            raise ValueError(f"Missing 'integrator' key in {d}.")
        
        import lammpsinputbuilder.loader.integratorLoader as loader
        integratorLoader = loader.IntegratorLoader()
        self.integrator = integratorLoader.dictToIntegrator(d["integrator"], version)
        
    def addAllCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        result =  "################# START SECTION " + self.sectionName + " #################\n\n"
        result += self.addDoCommands()
        result += self.integrator.addRunCommands()
        result += self.addUndoCommands()
        result += "################# END SECTION " + self.sectionName + " #################\n\n"
        return result

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        result = ""
        for io in self.fileIOs:
            result += io.addDoCommands(unitsystem)
        result += self.integrator.addDoCommands(unitsystem)
        return result
    
    def addUndoCommands(self) -> str:
        # Undo if the reverse order is needed
        result = ""
        result += self.integrator.addUndoCommands()
        for io in reversed(self.fileIOs):
            result += io.addUndoCommands()
        return result

class InstructionsSection(Section):
    def __init__(self) -> None:
        super().__init__()
        self.instructions: List[Instruction] = []

    def addInstruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["instructions"] = [c.toDict() for c in self.instructions]
        return result
    
    def fromDict(self, d: dict, version: int):
        super().fromDict(d, version=version)
        instructionsDict = d.get("instructions", [])
        if len(instructionsDict) > 0:
            import lammpsinputbuilder.loader.instructionLoader as loader
        
            instructionLoader = loader.InstructionLoader()
            self.instructions = [instructionLoader.dictToInstruction(c, version) for c in instructionsDict]

    def addAllCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        result =  "################# START SECTION " + self.sectionName + " #################\n\n"
        for instruction in self.instructions:
            result += instruction.writeInstruction(unitsystem)
        result += "################# END SECTION " + self.sectionName + " #################\n\n"
        return result