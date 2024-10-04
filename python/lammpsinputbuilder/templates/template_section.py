"""
Module implementing a template for sections.
"""

from typing import List

from lammpsinputbuilder.fileio import FileIO
from lammpsinputbuilder.group import Group
from lammpsinputbuilder.section import Section
from lammpsinputbuilder.extensions import Extension
from lammpsinputbuilder.instructions import Instruction
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.utility.string_utils import write_fixed_length_comment



class TemplateSection(Section):
    def __init__(self, section_name: str = "defaultSection") -> None:
        super().__init__(section_name=section_name)
        self.ios: List[FileIO] = []
        self.extensions: List[Extension] = []
        self.groups: List[Group] = []
        self.instructions: List[Instruction] = []

    def add_fileio(self, fileio: FileIO):
        self.ios.append(fileio)

    def get_fileios(self) -> List[FileIO]:
        return self.ios

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        return self.instructions

    def add_extension(self, extension: Extension):
        self.extensions.append(extension)

    def get_extensions(self) -> List[Extension]:
        return self.extensions

    def add_group(self, group: Group):
        self.groups.append(group)

    def get_groups(self) -> List[Group]:
        return self.groups

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["fileios"] = [s.to_dict() for s in self.ios]
        result["extensions"] = [s.to_dict() for s in self.extensions]
        result["groups"] = [s.to_dict() for s in self.groups]
        result["instructions"] = [s.to_dict() for s in self.instructions]
        return result

    def from_dict(self, d: dict, version: int):
        super().from_dict(d, version=version)

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
                self.instructions.append(loader.dict_to_instruction(
                    instruction, version))

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
        sections = self.generate_sections()
        for section in sections:
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

    def generate_sections(self) -> List[Section]:
        raise NotImplementedError(
            "The class {self.__class__.__name__} cannot be used directly. \
            Please use a subclass and implement the function generate_sections() \
            or override the function add_all_commands().")
