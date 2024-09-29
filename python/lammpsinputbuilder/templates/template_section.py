"""
Module implementing a template for sections.
"""

from typing import List

from lammpsinputbuilder.fileio import FileIO
from lammpsinputbuilder.group import Group
from lammpsinputbuilder.section import Section
from lammpsinputbuilder.extensions import Extension
from lammpsinputbuilder.types import GlobalInformation



class TemplateSection(Section):
    def __init__(self, section_name: str = "defaultSection") -> None:
        super().__init__(section_name=section_name)
        self.ios: List[FileIO] = []
        self.extensions: List[Extension] = []
        self.groups: List[Group] = []

    def add_fileio(self, fileio: FileIO):
        self.ios.append(fileio)

    def add_extension(self, extension: Extension):
        self.extensions.append(extension)

    def add_group(self, group: Group):
        self.groups.append(group)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["fileios"] = [s.to_dict() for s in self.ios]
        result["extensions"] = [s.to_dict() for s in self.extensions]
        result["groups"] = [s.to_dict() for s in self.groups]
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
        sections = self.generate_sections()
        for section in sections:
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

    def generate_sections(self) -> List[Section]:
        raise NotImplementedError(
            "The class {self.__class__.__name__} cannot be used directly. \
            Please use a subclass and implement the function generate_sections() \
            or override the function add_all_commands().")
