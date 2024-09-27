"""
Module implementing a template for sections.
"""

from typing import List

from lammpsinputbuilder.fileIO import FileIO
from lammpsinputbuilder.group import Group
from lammpsinputbuilder.section import Section
from lammpsinputbuilder.extensions import Extension
from lammpsinputbuilder.types import GlobalInformation



class TemplateSection(Section):
    def __init__(self, sectionName: str = "defaultSection") -> None:
        super().__init__(sectionName=sectionName)
        self.ios: List[FileIO] = []
        self.extensions: List[Extension] = []
        self.groups: List[Group] = []

    def addFileIO(self, fileIO: FileIO):
        self.ios.append(fileIO)

    def addExtension(self, extension: Extension):
        self.extensions.append(extension)

    def addGroup(self, group: Group):
        self.groups.append(group)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["fileIOs"] = [s.toDict() for s in self.ios]
        result["extensions"] = [s.toDict() for s in self.extensions]
        result["groups"] = [s.toDict() for s in self.groups]
        return result

    def fromDict(self, d: dict, version: int):
        super().fromDict(d, version=version)

        if "fileIOs" in d.keys() and len(d["fileIOs"]) > 0:
            ios = d["fileIOs"]

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

    def addAllCommands(self, globalInformation: GlobalInformation) -> str:
        # Declare all the objects which are going to live during the entire
        # duractions of the sections
        result = f"################# START Section {self.sectionName} #################\n"
        result += "################# START Groups DECLARATION #################\n"
        for grp in self.groups:
            result += grp.addDoCommands()
        result += "################# END Groups DECLARATION #################\n"

        result += "################# START Extensions DECLARATION #################\n"
        for ext in self.extensions:
            result += ext.addDoCommands(globalInformation=globalInformation)
        result += "################# END Extensions DECLARATION #################\n"

        result += "################# START IOs DECLARATION #################\n"
        for io in self.ios:
            result += io.addDoCommands(globalInformation=globalInformation)
        result += "################# END IOs DECLARATION #################\n"

        # Everything is declared, now we can execute the differente sections
        sections = self.generateSections()
        for section in sections:
            result += section.addAllCommands(
                globalInformation=globalInformation)

        # Everything is executed, now we can undo the differente sections
        result += "################# START IO REMOVAL #################\n"
        for io in reversed(self.ios):
            result += io.addUndoCommands()
        result += "################# END IOs DECLARATION #################\n"

        result += "################# START Extensions REMOVAL #################\n"
        for ext in reversed(self.extensions):
            result += ext.addUndoCommands()
        result += "################# END Extensions DECLARATION #################\n"

        result += "################# START Groups REMOVAL #################\n"
        for grp in reversed(self.groups):
            result += grp.addUndoCommands()
        result += "################# END Groups DECLARATION #################\n"

        result += f"################# END Section {self.sectionName} #################\n"

        return result

    def generateSections(self) -> List[Section]:
        raise NotImplementedError(
            "The class {self.__class__.__name__} cannot be used directly. Please use a subclass and implement the function generateSections() or override the function addAllCommands().")
