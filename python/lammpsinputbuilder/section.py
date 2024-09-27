"""Module implementing the Section class and its subclasses."""

from typing import List

from lammpsinputbuilder.integrator import Integrator, RunZeroIntegrator
from lammpsinputbuilder.fileIO import FileIO
from lammpsinputbuilder.instructions import Instruction
from lammpsinputbuilder.extensions import Extension
from lammpsinputbuilder.group import Group
from lammpsinputbuilder.types import GlobalInformation


class Section:
    def __init__(self, section_name: str = "defaultSection") -> None:
        self.section_name = section_name

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["section_name"] = self.section_name
        return result

    def from_dict(self, d: dict):
        self.section_name = d.get("section_name", "defaultSection")
        return

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        result += self.add_do_commands(global_information=global_information)
        result += self.add_undo_commands()
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class RecusiveSection(Section):
    def __init__(self, section_name: str = "defaultSection") -> None:
        super().__init__(section_name=section_name)
        self.sections: List[Section] = []
        self.ios: List[FileIO] = []
        self.extensions: List[Extension] = []
        self.groups: List[Group] = []

    def add_section(self, section: Section):
        self.sections.append(section)

    def add_fileio(self, fileio: FileIO):
        self.ios.append(fileio)

    def add_extension(self, extension: Extension):
        self.extensions.append(extension)

    def add_group(self, group: Group):
        self.groups.append(group)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["sections"] = [s.to_dict() for s in self.sections]
        result["fileios"] = [s.to_dict() for s in self.ios]
        result["extensions"] = [s.to_dict() for s in self.extensions]
        result["groups"] = [s.to_dict() for s in self.groups]
        return result

    def from_dict(self, d: dict, version: int):
        super().from_dict(d, version=version)

        if "sections" in d.keys() and len(d["sections"]) > 0:
            sections = d["sections"]

            from lammpsinputbuilder.loader.sectionLoader import SectionLoader
            loader = SectionLoader()

            for section in sections:
                self.sections.append(loader.dict_to_section(section))

        if "fileios" in d.keys() and len(d["fileios"]) > 0:
            ios = d["fileios"]

            from lammpsinputbuilder.loader.fileIOLoader import FileIOLoader
            loader = FileIOLoader()

            for io in ios:
                self.ios.append(loader.dict_to_fileio(io))

        if "extensions" in d.keys() and len(d["extensions"]) > 0:
            exts = d["extensions"]

            from lammpsinputbuilder.loader.extensionLoader import ExtensionLoader
            loader = ExtensionLoader()

            for ext in exts:
                self.extensions.append(loader.dict_to_extension(ext))

        if "groups" in d.keys() and len(d["groups"]) > 0:
            groups = d["groups"]

            from lammpsinputbuilder.loader.groupLoader import GroupLoader
            loader = GroupLoader()

            for group in groups:
                self.groups.append(loader.dict_to_group(group))

    def add_all_commands(self, global_information: GlobalInformation) -> str:

        # Declare all the objects which are going to live during the entire
        # duractions of the sections
        result = f"################# START Section {self.section_name} #################\n"
        result += "################# START Groups DECLARATION #################\n"
        for grp in self.groups:
            result += grp.add_do_commands()
        result += "################# END Groups DECLARATION #################\n"

        result += "################# START Extensions DECLARATION #################\n"
        for ext in self.extensions:
            result += ext.add_do_commands(global_information=global_information)
        result += "################# END Extensions DECLARATION #################\n"

        result += "################# START IOs DECLARATION #################\n"
        for io in self.ios:
            result += io.add_do_commands(global_information=global_information)
        result += "################# END IOs DECLARATION #################\n"

        # Everything is declared, now we can execute the differente sections
        for section in self.sections:
            result += section.add_all_commands(
                global_information=global_information)

        # Everything is executed, now we can undo the differente sections
        result += "################# START IO REMOVAL #################\n"
        for io in reversed(self.ios):
            result += io.add_undo_commands()
        result += "################# END IOs DECLARATION #################\n"

        result += "################# START Extensions REMOVAL #################\n"
        for ext in reversed(self.extensions):
            result += ext.add_undo_commands()
        result += "################# END Extensions DECLARATION #################\n"

        result += "################# START Groups REMOVAL #################\n"
        for grp in reversed(self.groups):
            result += grp.add_undo_commands()
        result += "################# END Groups DECLARATION #################\n"

        result += f"################# END Section {self.section_name} #################\n"

        return result


class IntegratorSection(Section):
    def __init__(self, section_name: str = "defaultSection",
                 integrator: Integrator = RunZeroIntegrator()) -> None:
        super().__init__(section_name=section_name)
        self.integrator = integrator
        self.fileios = []
        self.extensions = []
        self.groups = []

    def getIntegrator(self) -> Integrator:
        return self.integrator

    def setIntegrator(self, integrator: Integrator) -> None:
        self.integrator = integrator

    def add_fileio(self, fileio: FileIO) -> None:
        self.fileios.append(fileio)

    def add_extension(self, extension: Extension) -> None:
        self.extensions.append(extension)

    def add_group(self, group: Group) -> None:
        self.groups.append(group)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["integrator"] = self.integrator.to_dict()
        result["fileios"] = [f.to_dict() for f in self.fileios]
        result["extensions"] = [e.to_dict() for e in self.extensions]
        result["groups"] = [g.to_dict() for g in self.groups]
        return result

    def from_dict(self, d: dict, version: int) -> None:
        super().from_dict(d, version=version)
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        if "integrator" not in d.keys():
            raise ValueError(f"Missing 'integrator' key in {d}.")

        import lammpsinputbuilder.loader.integratorLoader as loader
        integratorLoader = loader.IntegratorLoader()
        self.integrator = integratorLoader.dictToIntegrator(
            d["integrator"], version)

        if "fileios" in d.keys() and len(d["fileios"]) > 0:
            ios = d["fileios"]

            import lammpsinputbuilder.loader.fileIOLoader as loader
            fileIOLoader = loader.FileIOLoader()

            for io in ios:
                self.fileios.append(fileIOLoader.dictToFileIO(io))

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
                self.groups.append(groupLoader.dict_to_group(group))

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        result = "################# START SECTION " + \
            self.section_name + " #################\n\n"
        result += self.add_do_commands(global_information=global_information)
        result += "################# START RUN INTEGRATOR FOR SECTION " + \
            self.section_name + " #################\n"
        result += self.integrator.addRunCommands()
        result += "################# END RUN INTEGRATOR FOR SECTION " + \
            self.section_name + " #################\n"
        result += self.add_undo_commands()
        result += "################# END SECTION " + \
            self.section_name + " #################\n\n"
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        result += "################# START Groups DECLARATION #################\n"
        for grp in self.groups:
            result += grp.add_do_commands()
        result += "################# END Groups DECLARATION #################\n"

        result += "################# START Extensions DECLARATION #################\n"
        for ext in self.extensions:
            result += ext.add_do_commands(global_information=global_information)
        result += "################# END Extensions DECLARATION #################\n"

        result += "################# START IOs DECLARATION #################\n"
        for io in self.fileios:
            result += io.add_do_commands(global_information=global_information)
        result += "################# END IOs DECLARATION #################\n"

        result += "################# START INTEGRATOR DECLARATION #################\n"
        result += self.integrator.add_do_commands(
            global_information=global_information)
        result += "################# END INTEGRATOR DECLARATION #################\n"
        return result

    def add_undo_commands(self) -> str:
        # Undo if the reverse order is needed
        result = ""
        result += "################# START INTEGRATOR REMOVAL #################\n"
        result += self.integrator.add_undo_commands()
        result += "################# END INTEGRATOR REMOVAL #################\n"

        result += "################# START IO REMOVAL #################\n"
        for io in reversed(self.fileios):
            result += io.add_undo_commands()
        result += "################# END IOs DECLARATION #################\n"

        result += "################# START Extensions REMOVAL #################\n"
        for ext in reversed(self.extensions):
            result += ext.add_undo_commands()
        result += "################# END Extensions DECLARATION #################\n"

        result += "################# START Groups REMOVAL #################\n"
        for grp in reversed(self.groups):
            result += grp.add_undo_commands()
        result += "################# END Groups DECLARATION #################\n"

        return result


class InstructionsSection(Section):
    def __init__(self, section_name: str = "defaultSection") -> None:
        super().__init__(section_name=section_name)
        self.instructions: List[Instruction] = []

    def addInstruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["instructions"] = [c.to_dict() for c in self.instructions]
        return result

    def from_dict(self, d: dict, version: int):
        super().from_dict(d, version=version)
        instructionsDict = d.get("instructions", [])
        if len(instructionsDict) > 0:
            import lammpsinputbuilder.loader.instructionLoader as loader

            instructionLoader = loader.InstructionLoader()
            self.instructions = [
                instructionLoader.dict_to_instruction(
                    c, version) for c in instructionsDict]

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        result = "################# START SECTION " + \
            self.section_name + " #################\n\n"
        for instruction in self.instructions:
            result += instruction.write_instruction(
                global_information=global_information)
        result += "################# END SECTION " + \
            self.section_name + " #################\n\n"
        return result
