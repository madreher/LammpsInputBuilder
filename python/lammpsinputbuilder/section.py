from typing import List

from lammpsinputbuilder.integrator import Integrator, RunZeroIntegrator
from lammpsinputbuilder.fileIO import FileIO
from lammpsinputbuilder.quantities import LammpsUnitSystem
from lammpsinputbuilder.instructions import Instruction
from lammpsinputbuilder.extensions import Extension
from lammpsinputbuilder.group import Group

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
    
    def addAllCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        result = ""
        result += self.addDoCommands(unitsystem=unitsystem)
        result += self.addUndoCommands()
        return result
    
    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        return ""
    
    def addUndoCommands(self) -> str:
        return ""
    


class RecusiveSection(Section):
    def __init__(self, sectionName: str = "defaultSection") -> None:
        super().__init__(sectionName=sectionName)
        self.sections: List[Section] = []
        self.ios: List[FileIO] = []
        self.extensions: List[Extension] = []
        self.groups: List[Group] = []

    def addSection(self, section: Section):
        self.sections.append(section)

    def addFileIO(self, fileIO: FileIO):
        self.ios.append(fileIO)

    def addExtension(self, extension: Extension):
        self.extensions.append(extension)

    def addGroup(self, group: Group):
        self.groups.append(group)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["sections"] = [s.toDict() for s in self.sections]
        result["fileIOs"] = [s.toDict() for s in self.ios]
        result["extensions"] = [s.toDict() for s in self.extensions]
        result["groups"] = [s.toDict() for s in self.groups]
        return result
    
    def fromDict(self, d: dict, version: int):
        super().fromDict(d, version=version)
        self.sections = [Section.fromDict(s) for s in d["sections"]]

        if "fileIOs" in d.keys() and len(d["fileIOs"]) > 0:
            ios = d["fileIOs"]
            
            from lammpsinputbuilder.loader.fileIOLoader import FileIOLoader
            loader = FileIOLoader()

            for io in ios:
                self.ios.append(loader.dictToFileIO(io))

        if "extensions" in d.keys() and len(d["extensions"]) > 0:
            exts = d["extensions"]
            
            from lammpsinputbuilder.loader.extensionLoader import ExtensionLoader
            loader = ExtensionLoader()

            for ext in exts:
                self.extensions.append(loader.dictToExtension(ext))

        if "groups" in d.keys() and len(d["groups"]) > 0:
            groups = d["groups"]
            
            from lammpsinputbuilder.loader.groupLoader import GroupLoader
            loader = GroupLoader()

            for group in groups:
                self.groups.append(loader.dictToGroup(group))

    def addAllCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        
        # Declare all the objects which are going to live during the entire duractions of the sections
        result = f"################# START Section {self.sectionName} #################\n"
        result +=  "################# START Groups DECLARATION #################\n"
        for grp in self.groups:
            result += grp.addDoCommands()
        result +=  "################# END Groups DECLARATION #################\n"
        
        result +=  "################# START Extensions DECLARATION #################\n"
        for ext in self.extensions:
            result += ext.addDoCommands(unitsystem)
        result +=  "################# END Extensions DECLARATION #################\n"
        
        result +=  "################# START IOs DECLARATION #################\n"
        for io in self.ios:
            result += io.addDoCommands()
        result +=  "################# END IOs DECLARATION #################\n"
        
        # Everything is declared, now we can execute the differente sections
        for section in self.sections:
            result += section.addAllCommands(unitsystem=unitsystem)

        # Everything is executed, now we can undo the differente sections
        result +=  "################# START IO REMOVAL #################\n"
        for io in reversed(self.ios):
            result += io.addUndoCommands()
        result +=  "################# END IOs DECLARATION #################\n"
        
        result +=  "################# START Extensions REMOVAL #################\n"
        for ext in reversed(self.extensions):
            result += ext.addUndoCommands()
        result +=  "################# END Extensions DECLARATION #################\n"
        
        result +=  "################# START Groups REMOVAL #################\n"
        for grp in reversed(self.groups):
            result += grp.addUndoCommands()
        result +=  "################# END Groups DECLARATION #################\n"

        result += f"################# END Section {self.sectionName} #################\n"

        return result

class IntegratorSection(Section):
    def __init__(self, sectionName: str = "defaultSection", integrator: Integrator = RunZeroIntegrator()) -> None:
        super().__init__(sectionName=sectionName)
        self.integrator = integrator
        self.fileIOs = []
        self.extensions = []
        self.groups = []

    def addFileIO(self, fileIO: FileIO) -> None:
        self.fileIOs.append(fileIO)

    def addExtension(self, extension: Extension) -> None:
        self.extensions.append(extension)

    def addGroup(self, group: Group) -> None:
        self.groups.append(group)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["integrator"] = self.integrator.toDict()
        result["fileIOs"] = [f.toDict() for f in self.fileIOs]
        result["extensions"] = [e.toDict() for e in self.extensions]
        result["groups"] = [g.toDict() for g in self.groups]
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        super().fromDict(d, version=version)
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        if "integrator" not in d.keys():
            raise ValueError(f"Missing 'integrator' key in {d}.")
        
        import lammpsinputbuilder.loader.integratorLoader as loader
        integratorLoader = loader.IntegratorLoader()
        self.integrator = integratorLoader.dictToIntegrator(d["integrator"], version)

        if "fileIOs" in d.keys() and len(d["fileIOs"]) > 0:
            ios = d["fileIOs"]

            import lammpsinputbuilder.loader.fileIOLoader as loader
            fileIOLoader = loader.FileIOLoader()

            for io in ios:
                self.fileIOs.append(fileIOLoader.dictToFileIO(io))

        if "extensions" in d.keys() and len(d["extensions"]) > 0:
            exts = d["extensions"]

            import lammpsinputbuilder.loader.extensionLoader as loader
            extensionLoader = loader.ExtensionLoader()

            for ext in exts:
                self.extensions.append(extensionLoader.dictToExtension(ext))

        if "groups" in d.keys() and len(d["groups"]) > 0:
            groups = d["groups"]

            import lammpsinputbuilder.loader.groupLoader as loader
            groupLoader = loader.GroupLoader()

            for group in groups:
                self.groups.append(groupLoader.dictToGroup(group))

            
        
    def addAllCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        result =  "################# START SECTION " + self.sectionName + " #################\n\n"
        result += self.addDoCommands(unitsystem)
        result +=  "################# START RUN INTEGRATOR FOR SECTION " + self.sectionName + " #################\n"
        result += self.integrator.addRunCommands()
        result +=  "################# END RUN INTEGRATOR FOR SECTION " + self.sectionName + " #################\n"
        result += self.addUndoCommands()
        result += "################# END SECTION " + self.sectionName + " #################\n\n"
        return result

    def addDoCommands(self, unitsystem: LammpsUnitSystem = LammpsUnitSystem.REAL) -> str:
        result = ""
        result +=  "################# START Groups DECLARATION #################\n"
        for grp in self.groups:
            result += grp.addDoCommands()
        result +=  "################# END Groups DECLARATION #################\n"
        
        result +=  "################# START Extensions DECLARATION #################\n"
        for ext in self.extensions:
            result += ext.addDoCommands(unitsystem)
        result +=  "################# END Extensions DECLARATION #################\n"
        
        result +=  "################# START IOs DECLARATION #################\n"
        for io in self.fileIOs:
            result += io.addDoCommands()
        result +=  "################# END IOs DECLARATION #################\n"
        
        result +=  "################# START INTEGRATOR DECLARATION #################\n"
        result += self.integrator.addDoCommands(unitsystem)
        result +=  "################# END INTEGRATOR DECLARATION #################\n"
        return result
    
    def addUndoCommands(self) -> str:
        # Undo if the reverse order is needed
        result = ""
        result +=  "################# START INTEGRATOR REMOVAL #################\n"
        result += self.integrator.addUndoCommands()
        result +=  "################# END INTEGRATOR REMOVAL #################\n"
        
        result +=  "################# START IO REMOVAL #################\n"
        for io in reversed(self.fileIOs):
            result += io.addUndoCommands()
        result +=  "################# END IOs DECLARATION #################\n"
        
        result +=  "################# START Extensions REMOVAL #################\n"
        for ext in reversed(self.extensions):
            result += ext.addUndoCommands()
        result +=  "################# END Extensions DECLARATION #################\n"
        
        result +=  "################# START Groups REMOVAL #################\n"
        for grp in reversed(self.groups):
            result += grp.addUndoCommands()
        result +=  "################# END Groups DECLARATION #################\n"

        return result

class InstructionsSection(Section):
    def __init__(self, sectionName: str = "defaultSection") -> None:
        super().__init__(sectionName=sectionName)
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