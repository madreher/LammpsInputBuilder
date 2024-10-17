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
    """
    Base class for all the sections. A section represents a series of commands
    which have a scope. We define a scope in Lammps as the time between the registration 
    of a command and when it is unregistered. 

    A lot of objects in LammpsInputBuilder have a do and undo command. For such object, the do 
    commands would be executed at the start of the section and the undo commands would be executed 
    at the end of the section, thus defining a scope.

    The one exception to this approach are the Instruction objects which do not have a scope and could be called at 
    any time within a section.

    Note that a Section in LammpsInputBuilder doesn't represent any native Lammps functionality. It is meant as an 
    abstraction to represent the life time of Lammps commands and ensure that every object declared 
    within a Lammps script gets removed at the right time.
    """

    def __init__(self, section_name: str = "defaultSection") -> None:
        """
        Constructor for the Section class.
        Args:
            section_name (str): The name of the section. The name must be alpha numeric
                                and start with a letter
        Returns:
            None
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(id_name=section_name)

    def get_section_name(self) -> str:
        """
        Returns the name of the section
        Returns:
            str: The name of the section
        """
        return super().get_id_name()

    def set_section_name(self, section_name: str):
        """
        Set the name of the section
        Args:
            section_name (str): The name of the section
        Returns:
            None
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().set_id_name(id_name=section_name)
        self.validate_id()

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the section
        Returns:
            dict: The dictionary representation of the section
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        """
        Returns the string representation of the section
        Args:
            global_information (GlobalInformation): The global information
        Returns:
            str: The string representation of the section
        """
        result = ""
        result += self.add_do_commands(global_information=global_information)
        result += self.add_undo_commands()
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Returns the string representation of the section
        Args:
            global_information (GlobalInformation): The global information
        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        return ""

    def add_undo_commands(self) -> str:
        """
        Returns the string representation of the section
        Returns:
            str: Lammps command(s)
        """
        return ""


class RecursiveSection(Section):
    """
    Class for the recursive section. A recursive section allows the user to declare 
    groups, extensions, instructions, and fileio objects which are going to be in scope for
    multiple sections.

    For example, in the case of FileIOs object, the RecursiveSection allows the user to define a 
    trajectory which is going to produces a single trajectory files spanning across multiple sections.

    The RecursiveSection generate Lammps commands as follow:
    * Do list of Groups
    * Do list of Instructions
    * Do list of Extensions
    * Do list of FileIO
    * All Sections
    * Undo reverse list of FileIO
    * Undo reverse list of Extensions
    * Undo reverse list of Groups
    """
    def __init__(self, section_name: str = "defaultSection") -> None:
        """
        Constructor
        Args:
            section_name (str): The name of the section. The name must be alpha numeric
                                and start with a letter
        Returns:
            None
        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(section_name=section_name)
        self.sections: List[Section] = []
        self.ios: List[FileIO] = []
        self.extensions: List[Extension] = []
        self.groups: List[Group] = []
        self.instructions: List[Instruction] = []

    def add_section(self, section: Section):
        """
        Add a section to the section list
        Args:
            section (Section): The section to add
        """
        self.sections.append(section)

    def get_sections(self) -> List[Section]:
        """
        Returns the list of sections
        Returns:
            List[Section]: The list of sections
        """
        return self.sections

    def add_fileio(self, fileio: FileIO):
        """
        Add a fileio to the fileio list
        Args:
            fileio (FileIO): The fileio to add
        """
        self.ios.append(fileio)

    def get_fileios(self) -> List[FileIO]:
        """
        Returns the list of fileio
        Returns:
            List[FileIO]: The list of fileio
        """
        return self.ios

    def add_extension(self, extension: Extension):
        """
        Add an extension to the extension list
        Args:
            extension (Extension): The extension to add
        """
        self.extensions.append(extension)

    def get_extensions(self) -> List[Extension]:
        """
        Returns the list of extensions
        Returns:
            List[Extension]: The list of extensions
        """
        return self.extensions

    def add_group(self, group: Group):
        """
        Add a group to the group list
        Args:
            group (Group): The group to add
        """
        self.groups.append(group)

    def get_groups(self) -> List[Group]:
        """
        Returns the list of groups
        Returns:
            List[Group]: The list of groups
        """
        return self.groups
    
    def add_instruction(self, instruction: Instruction):
        """
        Add an instruction to the instruction list
        Args:
            instruction (Instruction): The instruction to add
        """
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        """
        Returns the list of instructions
        Returns:
            List[Instruction]: The list of instructions
        """
        return self.instructions

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the section
        Returns:
            dict: The dictionary representation of the section
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["sections"] = [s.to_dict() for s in self.sections]
        result["fileios"] = [s.to_dict() for s in self.ios]
        result["extensions"] = [s.to_dict() for s in self.extensions]
        result["groups"] = [s.to_dict() for s in self.groups]
        result["instructions"] = [s.to_dict() for s in self.instructions]
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the section and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the section.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or the same as the current class
        """
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
        """
        Add all the commands of the section
        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: Lammps command(s)
        """

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
    """
    The IntegratorSection is the base class to run a time integration simulation.
    This Section is built around an Integrator object and allow the user to declare 
    groups, instructions, extensions, and fileios which are going to be active during the 
    execution of the integrator. These objects are then removed at the end of the section.

    Note: some extension may require to be declare after the integration process, for example 
    after the declaration of a nve. For this purpose, the method `add_post_extension()` allows user 
    to add extensions which will be declared after the integration method.

    The IntegratorSection produces Lammps commands in the following order:
    * Do list of Groups
    * Do list of Instructions
    * Do list of Extensions
    * Do Integrator
    * Do list of post Extensions
    * Do list of FileIO
    * Run Integrator
    * Undo reverse list of FileIO
    * Undo reverse list of post Extensions
    * Undo Integrator
    * Undo reverse list of Extensions
    * Undo reverse list of Groups
    """
    def __init__(self, section_name: str = "defaultSection",
                 integrator: Integrator = RunZeroIntegrator()) -> None:
        """
        Constructor
        Args:
            section_name (str): The name of the section
            integrator (Integrator): The integrator object

        Returns:
            None
        """
        super().__init__(section_name=section_name)
        self.integrator = integrator
        self.fileios = []
        self.extensions = []
        self.post_extensions = []
        self.groups = []
        self.instructions = []

    def get_integrator(self) -> Integrator:
        """
        Get the integrator
        Returns:
            Integrator: The integrator
        """
        return self.integrator

    def set_integrator(self, integrator: Integrator) -> None:
        """
        Set the integrator
        Args:
            integrator (Integrator): The integrator

        Returns:
            None
        """
        self.integrator = integrator

    def add_fileio(self, fileio: FileIO) -> None:
        """
        Add a fileio
        Args:
            fileio (FileIO): The fileio to add

        Returns:
            None
        """
        self.fileios.append(fileio)

    def get_fileios(self) -> List[FileIO]:
        """
        Get the fileios
        Returns:
            List[FileIO]: The fileios
        """
        return self.fileios

    def add_extension(self, extension: Extension) -> None:
        """
        Add an extension
        Args:
            extension (Extension): The extension to add

        Returns:
            None
        """
        self.extensions.append(extension)

    def get_extensions(self) -> List[Extension]:
        """
        Get the extensions
        Returns:
            List[Extension]: The extensions
        """
        return self.extensions
    
    def add_post_extension(self, extension: Extension) -> None:
        """
        Add an extension which will be declared after the Integrator
        Args:
            extension (Extension): The extension to add

        Returns:
            None
        """
        self.post_extensions.append(extension)

    def get_post_extensions(self) -> List[Extension]:
        """
        Get the post extensions
        Returns:
            List[Extension]: The post extensions
        """
        return self.post_extensions

    def add_group(self, group: Group) -> None:
        """
        Add a group
        Args:
            group (Group): The group to add

        Returns:
            None
        """
        self.groups.append(group)

    def get_groups(self) -> List[Group]:
        """
        Get the groups
        Returns:
            List[Group]: The groups
        """
        return self.groups

    def add_instruction(self, instruction: Instruction) -> None:
        """
        Add an instruction
        Args:
            instruction (Instruction): The instruction to add

        Returns:
            None
        """
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        """
        Get the instructions
        Returns:
            List[Instruction]: The instructions
        """
        return self.instructions

    def to_dict(self) -> dict:
        """
        Get the dictionary representation of the section
        Returns:
            dict: The dictionary representation of the section
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["integrator"] = self.integrator.to_dict()
        result["fileios"] = [f.to_dict() for f in self.fileios]
        result["extensions"] = [e.to_dict() for e in self.extensions]
        result["post_extensions"] = [e.to_dict() for e in self.post_extensions]
        result["groups"] = [g.to_dict() for g in self.groups]
        result["instructions"] = [i.to_dict() for i in self.instructions]
        return result

    def from_dict(self, d: dict, version: int) -> None:
        """
        Initialize the section from the dictionary representation
        Args:
            d (dict): The dictionary representation of the section
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or the same as the current class
        """
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

        if "post_extensions" in d.keys() and len(d["post_extensions"]) > 0:
            exts = d["post_extensions"]

            import lammpsinputbuilder.loader.extension_loader as loader
            extension_loader = loader.ExtensionLoader()

            for ext in exts:
                self.post_extensions.append(extension_loader.dict_to_extension(ext))

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
        """
        Add all the commands from the section.
        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: Lammps command(s)
        """
        result = write_fixed_length_comment(f"START SECTION {self.get_section_name()}")
        result += self.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment(f"START RUN INTEGRATOR FOR SECTION {self.get_section_name()}")
        result += self.integrator.add_run_commands()
        result += write_fixed_length_comment(f"END RUN INTEGRATOR FOR SECTION {self.get_section_name()}")
        result += self.add_undo_commands()
        result += write_fixed_length_comment(f"END SECTION {self.get_section_name()}")
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Add the do commands from the section.
        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: Lammps command(s)
        """
        result = ""
        result += write_fixed_length_comment("START Groups DECLARATION")
        for grp in self.groups:
            result += grp.add_do_commands()
        result += write_fixed_length_comment("END Groups DECLARATION")

        result += write_fixed_length_comment("START Extensions DECLARATION")
        for ext in self.extensions:
            result += ext.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END Extensions DECLARATION")

        result += write_fixed_length_comment("START INTEGRATOR DECLARATION")
        result += self.integrator.add_do_commands(
            global_information=global_information)
        result += write_fixed_length_comment("END INTEGRATOR DECLARATION")

        result += write_fixed_length_comment("START Post Extensions DECLARATION")
        for ext in self.post_extensions:
            result += ext.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END Post Extensions DECLARATION")

        result += write_fixed_length_comment("START IOs DECLARATION")
        for io in self.fileios:
            result += io.add_do_commands(global_information=global_information)
        result += write_fixed_length_comment("END IOs DECLARATION")

        return result

    def add_undo_commands(self) -> str:
        """
        Add the undo commands from the section.

        Returns:
            str: Lammps command(s)
        """
        # Undo if the reverse order is needed
        result = ""

        result += write_fixed_length_comment("START IO REMOVAL")
        for io in reversed(self.fileios):
            result += io.add_undo_commands()
        result += write_fixed_length_comment("END IOs DECLARATION")

        result += write_fixed_length_comment("START Post Extensions REMOVAL")
        for ext in reversed(self.post_extensions):
            result += ext.add_undo_commands()
        result += write_fixed_length_comment("END Post Extensions REMOVAL")

        result += write_fixed_length_comment("START INTEGRATOR REMOVAL")
        result += self.integrator.add_undo_commands()
        result += write_fixed_length_comment("END INTEGRATOR REMOVAL")

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
    """
    The InstructionsSection is meant to execute instructions outside the scope of 
    regular sections or time integration processes. An InstructionsSection is typically used 
    as an intermediate step in a workflow to modify the current state of the simulation before 
    continuin the simulation process.

    Note: This type of Section object is the only one which doesn't have a scope associated to it.
    Consequently, this section only accept Instructions objects as these are the only objects which 
    do not have a scope.
    """
    def __init__(self, section_name: str = "defaultSection") -> None:
        """
        Constructor

        Args:
            section_name (str, optional): The name of the section. Defaults to "defaultSection".
        Returns:
            None

        Raise:
            ValueError: If the name of the section is not alphanumeric
        """
        super().__init__(section_name=section_name)
        self.instructions: List[Instruction] = []

    def add_instruction(self, instruction: Instruction):
        """
        Add an instruction to the section

        Args:
            instruction (Instruction): The instruction to add

        Returns:
            None
        """
        self.instructions.append(instruction)

    def get_instructions(self) -> List[Instruction]:
        """
        Get the instructions of the section

        Returns:
            List[Instruction]: The list of instructions
        """
        return self.instructions

    def to_dict(self) -> dict:
        """
        Convert the section to a dictionary representation

        Returns:
            dict: The dictionary representation of the section
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["instructions"] = [c.to_dict() for c in self.instructions]
        return result

    def from_dict(self, d: dict, version: int):
        """
        Load the section from a dictionary representation

        Args:
            d (dict): The dictionary representation of the section
            version (int): The version of the section
        Returns:
            None
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
        
        """
        super().from_dict(d, version=version)
        instructions_dict = d.get("instructions", [])
        if len(instructions_dict) > 0:
            import lammpsinputbuilder.loader.instruction_loader as loader

            instruction_loader = loader.InstructionLoader()
            self.instructions = [
                instruction_loader.dict_to_instruction(
                    c, version) for c in instructions_dict]

    def add_all_commands(self, global_information: GlobalInformation) -> str:
        """
        Add the commands for the section.

        Args:
            global_information (GlobalInformation): The global information of the simulation

        Returns:
            str: Lammps command(s)
        """
        result = write_fixed_length_comment(f"START SECTION {self.get_section_name()}")
        for instruction in self.instructions:
            result += instruction.write_instruction(
                global_information=global_information)
        result += write_fixed_length_comment(f"END SECTION {self.get_section_name()}")
        return result
