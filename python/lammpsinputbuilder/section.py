"""Module implementing the Section class and its subclasses."""

from typing import List

from lammpsinputbuilder.integrator import Integrator, RunZeroIntegrator
from lammpsinputbuilder.fileio import FileIO
from lammpsinputbuilder.instructions import Instruction
from lammpsinputbuilder.extensions import Extension
from lammpsinputbuilder.group import Group
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.base import BaseObject
from lammpsinputbuilder.utility.string_utils import write_fixed_length_comment


class Section(BaseObject):
    def __init__(self, section_name: str = "defaultSection") -> None:
        super().__init__(id_name=section_name)

    def get_section_name(self) -> str:
        return super().get_id_name()

    def set_section_name(self, section_name: str):
        super().set_id_name(id_name=section_name)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        result += self.add_do_commands(global_information=global_information)
        result += self.add_undo_commands()
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        del global_information  # unused
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
        self.instructions: List[Instruction] = []

    def add_section(self, section: Section):
        self.sections.append(section)

    def get_sections(self) -> List[Section]:
        return self.sections

    def add_fileio(self, fileio: FileIO):
        self.ios.append(fileio)

    def get_fileios(self) -> List[FileIO]:
        return self.ios

    def add_extension(self, extension: Extension):
        self.extensions.append(extension)

    def get_extensions(self) -> List[Extension]:
        return self.extensions

    def add_group(self, group: Group):
        self.groups.append(group)

    def get_groups(self) -> List[Group]:
        return self.groups
    
    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        return self.instructions

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["sections"] = [s.to_dict() for s in self.sections]
        result["fileios"] = [s.to_dict() for s in self.ios]
        result["extensions"] = [s.to_dict() for s in self.extensions]
        result["groups"] = [s.to_dict() for s in self.groups]
        result["instructions"] = [s.to_dict() for s in self.instructions]
        return result

    def from_dict(self, d: dict, version: int):
        super().from_dict(d, version=version)

        if "sections" in d.keys() and len(d["sections"]) > 0:
            sections = d["sections"]

            from lammpsinputbuilder.loader.section_loader import SectionLoader
            loader = SectionLoader()

            for section in sections:
                self.sections.append(loader.dict_to_section(section))

        if "fileios" in d.keys() and len(d["fileios"]) > 0:
            ios = d["fileios"]

            from lammpsinputbuilder.loader.fileio_loader import FileIOLoader
            loader = FileIOLoader()

            for io in ios:
                self.ios.append(loader.dict_to_fileio(io))

        if "extensions" in d.keys() and len(d["extensions"]) > 0:
            exts = d["extensions"]

            from lammpsinputbuilder.loader.extension_loader import ExtensionLoader
            loader = ExtensionLoader()

            for ext in exts:
                self.extensions.append(loader.dict_to_extension(ext))

        if "groups" in d.keys() and len(d["groups"]) > 0:
            groups = d["groups"]

            from lammpsinputbuilder.loader.group_loader import GroupLoader
            loader = GroupLoader()

            for group in groups:
                self.groups.append(loader.dict_to_group(group))

        if "instructions" in d.keys() and len(d["instructions"]) > 0:
            instructions = d["instructions"]

            from lammpsinputbuilder.loader.instruction_loader import InstructionLoader
            loader = InstructionLoader()

            for instruction in instructions:
                self.instructions.append(loader.dict_to_instruction(instruction))

    def add_all_commands(self, global_information: GlobalInformation) -> str:

        # Declare all the objects which are going to live during the entire
        # duractions of the sections
        result = write_fixed_length_comment(f"START Section {self.get_section_name()}")
        result += write_fixed_length_comment("START Groups DECLARATION")
        for grp in self.groups:
            result += grp.add_do_commands()
        result += write_fixed_length_comment("END Groups DECLARATION")

        result += write_fixed_length_comment("START Extensions DECLARATION")
        for ext in self.extensions:
            result += ext.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END Extensions DECLARATION")

        result += write_fixed_length_comment("START IOs DECLARATION")
        for io in self.ios:
            result += io.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END IOs DECLARATION")

        # Everything is declared, now we can execute the differente sections
        for section in self.sections:
            result += section.add_all_commands(
                global_information=global_information)

        # Everything is executed, now we can undo the differente sections
        result += write_fixed_length_comment("START IO REMOVAL")
        for io in reversed(self.ios):
            result += io.add_undo_commands()
        result += write_fixed_length_comment("END IOs DECLARATION")

        result += write_fixed_length_comment("START Extensions REMOVAL")
        for ext in reversed(self.extensions):
            result += ext.add_undo_commands()
        result += write_fixed_length_comment("END Extensions DECLARATION")

        result += write_fixed_length_comment("START Groups REMOVAL")
        for grp in reversed(self.groups):
            result += grp.add_undo_commands()
        result += write_fixed_length_comment("END Groups DECLARATION")
        result += write_fixed_length_comment(f"END Section {self.get_section_name()}")

        return result


class IntegratorSection(Section):
    def __init__(self, section_name: str = "defaultSection",
                 integrator: Integrator = RunZeroIntegrator()) -> None:
        super().__init__(section_name=section_name)
        self.integrator = integrator
        self.fileios = []
        self.extensions = []
        self.groups = []
        self.instructions = []

    def get_integrator(self) -> Integrator:
        return self.integrator

    def set_integrator(self, integrator: Integrator) -> None:
        self.integrator = integrator

    def add_fileio(self, fileio: FileIO) -> None:
        self.fileios.append(fileio)

    def get_fileios(self) -> List[FileIO]:
        return self.fileios

    def add_extension(self, extension: Extension) -> None:
        self.extensions.append(extension)

    def get_extensions(self) -> List[Extension]:
        return self.extensions

    def add_group(self, group: Group) -> None:
        self.groups.append(group)

    def get_groups(self) -> List[Group]:
        return self.groups

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        return self.instructions

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["integrator"] = self.integrator.to_dict()
        result["fileios"] = [f.to_dict() for f in self.fileios]
        result["extensions"] = [e.to_dict() for e in self.extensions]
        result["groups"] = [g.to_dict() for g in self.groups]
        result["instructions"] = [i.to_dict() for i in self.instructions]
        return result

    def from_dict(self, d: dict, version: int) -> None:
        super().from_dict(d, version=version)
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        if "integrator" not in d.keys():
            raise ValueError(f"Missing 'integrator' key in {d}.")

        import lammpsinputbuilder.loader.integrator_loader as loader
        integrator_loader = loader.IntegratorLoader()
        self.integrator = integrator_loader.dict_to_integrator(
            d["integrator"], version)

        if "fileios" in d.keys() and len(d["fileios"]) > 0:
            ios = d["fileios"]

            import lammpsinputbuilder.loader.fileio_loader as loader
            fileio_loader = loader.FileIOLoader()

            for io in ios:
                self.fileios.append(fileio_loader.dict_to_fileio(io))

        if "extensions" in d.keys() and len(d["extensions"]) > 0:
            exts = d["extensions"]

            import lammpsinputbuilder.loader.extension_loader as loader
            extension_loader = loader.ExtensionLoader()

            for ext in exts:
                self.extensions.append(extension_loader.dict_to_extension(ext))

        if "groups" in d.keys() and len(d["groups"]) > 0:
            groups = d["groups"]

            import lammpsinputbuilder.loader.group_loader as loader
            group_loader = loader.GroupLoader()

            for group in groups:
                self.groups.append(group_loader.dict_to_group(group))

        if "instructions" in d.keys() and len(d["instructions"]) > 0:
            instructions = d["instructions"]

            import lammpsinputbuilder.loader.instruction_loader as loader
            instruction_loader = loader.InstructionLoader()

            for instruction in instructions:
                self.instructions.append(
                    instruction_loader.dict_to_instruction(instruction))

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        result = write_fixed_length_comment(f"START SECTION {self.get_section_name()}")
        result += self.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment(f"START RUN INTEGRATOR FOR SECTION {self.get_section_name()}")
        result += self.integrator.add_run_commands()
        result += write_fixed_length_comment(f"END RUN INTEGRATOR FOR SECTION {self.get_section_name()}")
        result += self.add_undo_commands()
        result += write_fixed_length_comment(f"END SECTION {self.get_section_name()}")
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        result = ""
        result += write_fixed_length_comment("START Groups DECLARATION")
        for grp in self.groups:
            result += grp.add_do_commands()
        result += write_fixed_length_comment("END Groups DECLARATION")

        result += write_fixed_length_comment("START Extensions DECLARATION")
        for ext in self.extensions:
            result += ext.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END Extensions DECLARATION")

        result += write_fixed_length_comment("START IOs DECLARATION")
        for io in self.fileios:
            result += io.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END IOs DECLARATION")

        result += write_fixed_length_comment("START INTEGRATOR DECLARATION")
        result += self.integrator.add_do_commands(
            global_information=global_information)
        result += write_fixed_length_comment("END INTEGRATOR DECLARATION")
        return result

    def add_undo_commands(self) -> str:
        # Undo if the reverse order is needed
        result = ""
        result += write_fixed_length_comment("START INTEGRATOR REMOVAL")
        result += self.integrator.add_undo_commands()
        result += write_fixed_length_comment("END INTEGRATOR REMOVAL")

        result += write_fixed_length_comment("START IO REMOVAL")
        for io in reversed(self.fileios):
            result += io.add_undo_commands()
        result += write_fixed_length_comment("END IOs DECLARATION")

        result += write_fixed_length_comment("START Extensions REMOVAL")
        for ext in reversed(self.extensions):
            result += ext.add_undo_commands()
        result += write_fixed_length_comment("END Extensions DECLARATION")

        result += write_fixed_length_comment("START Groups REMOVAL")
        for grp in reversed(self.groups):
            result += grp.add_undo_commands()
        result += write_fixed_length_comment("END Groups DECLARATION")

        return result


class InstructionsSection(Section):
    def __init__(self, section_name: str = "defaultSection") -> None:
        super().__init__(section_name=section_name)
        self.instructions: List[Instruction] = []

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        return self.instructions

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["instructions"] = [c.to_dict() for c in self.instructions]
        return result

    def from_dict(self, d: dict, version: int):
        super().from_dict(d, version=version)
        instructions_dict = d.get("instructions", [])
        if len(instructions_dict) > 0:
            import lammpsinputbuilder.loader.instruction_loader as loader

            instruction_loader = loader.InstructionLoader()
            self.instructions = [
                instruction_loader.dict_to_instruction(
                    c, version) for c in instructions_dict]

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        result = write_fixed_length_comment(f"START SECTION {self.get_section_name()}")
        for instruction in self.instructions:
            result += instruction.write_instruction(
                global_information=global_information)
        result += write_fixed_length_comment(f"END SECTION {self.get_section_name()}")
        return result
