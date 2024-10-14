"""WorkflowBuilder Module"""

from pathlib import Path
from uuid import uuid4
import shutil
import logging
import tempfile
from typing import List

from lammpsinputbuilder.typedmolecule import TypedMolecularSystem
from lammpsinputbuilder.section import Section
from lammpsinputbuilder.version import PackageVersion

logger = logging.getLogger(__name__)


class WorkflowBuilder:
    """
    The WorkflowBuilder is the entry point to define a workflow and generate 
    the corresponding Lammps input files. A workflow is define by a molecular 
    system and a sequence of sections to execute. If no section is provided,
    then Lammps inputs will only contains the declaration of the molecular system.
    """

    def __init__(self):
        """
        Initialize a new WorkflowBuilder.
        """
        self.molecule = None
        self.sections = []

    def set_typed_molecular_system(self, molecule: TypedMolecularSystem):
        """
        Set the molecular system to use.

        Args:
            molecule (TypedMolecularSystem): The molecular system to use.

        Returns: 
            None

        Raise:
            ValueError: If the molecule is not loaded.
        """
        if not molecule.is_model_loaded():
            raise ValueError(
                "The molecule must be loaded before it can be set.")
        self.molecule = molecule

    def get_typed_molecular_system(self) -> TypedMolecularSystem:
        """
        Get the molecular system currently set. If no molecular system is set,
        then None is returned.

        Returns:
            TypedMolecularSystem: The molecular system to use.
        """
        return self.molecule

    def add_section(self, section: Section):
        """
        Add a section to the workflow.

        Args:
            section (Section): The section to add.
        Returns:
            None
        """
        self.sections.append(section)

    def get_sections(self) -> List[Section]:
        """
        Get the list of sections currently set.

        Returns:
            List[Section]: The list of sections.
        """
        return self.sections

    def generate_inputs(self, job_folder_prefix: Path = None) -> Path:
        """
        Generate the input files for the workflow. This include a Lammps data file, 
        a Lammps input file, and a copy of the molecule file and the potential file 
        used to define the molecular system. 
        If the job_folder_prefix is not None, then a new job folder will be created in that folder. 
        Otherwise, tempfile.gettempdir() will be used as prefix.

        Args: 
            job_folder_prefix (Path): The prefix to use for the job folder.
        
        Returns:
            Path: The path to the folder with the generated input files.

        Raise:
            ValueError: If the molecule is not set.
        """


        if self.molecule is None:
            raise ValueError(
                "A molecule must be set before generating the input files. \
                See set_typed_molecular_system().")

        job_id = str(uuid4())

        prefix = job_folder_prefix
        if prefix is None:
            prefix = Path(tempfile.gettempdir())

        job_folder = prefix / job_id
        job_folder.mkdir(parents=True, exist_ok=True)
        logger.debug("WorkflowBuilder generated the job folder: %s", job_folder)

        # Write the initial Lammps files
        global_information = self.molecule.generate_lammps_data_file(job_folder)
        input_path = self.molecule.generate_lammps_input_file(
            job_folder, global_information)

        # System is now declared, we can add sections to the input file

        # First, we are going to copy the initial input file to a new file
        # This is to preserve the input file with the system declaration only
        # to help with debugging or additional manual analysis from the user
        workflow_input_path = job_folder / "workflow.input"
        shutil.copy(input_path, workflow_input_path)

        # Now we can add the sections
        section_content = ""
        for section in self.sections:
            section_content += section.add_all_commands(global_information)

        with open(workflow_input_path, "a", encoding="utf-8") as f:
            f.write(section_content)

        return job_folder

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the workflow.

        Returns:
            dict: The dictionary representation of the workflow.
        """
        result = {}
        result["header"] = {
            "format": self.__class__.__name__,
            "major_version": PackageVersion().get_major_lib_json_version(),
            "minor_version": PackageVersion().get_minor_lib_json_version(),
            "generator": "lammpsinputbuilder"
        }
        if self.molecule is not None:
            result["molecular_system"] = self.molecule.to_dict()

        if len(self.sections) > 0:
            result["sections"] = [s.to_dict() for s in self.sections]

        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the version is not supported.
            ValueError: If the header is not found
            ValueError: If the format is not found or supported.
            ValueError: If the major version is not found or supported.
            ValueError: If the minor version is not found or supported.
        """
        if version != 0:
            raise ValueError(f"Unsupported version {version}")

        del version  # unused

        if "header" not in d:
            raise ValueError("No header in JSON file, "
                             "unable to determine the format of the json file.")

        if "format" not in d["header"]:
            raise ValueError("No format in JSON file, "
                             "unable to determine the format of the json file.")

        if d["header"]["format"] != self.__class__.__name__:
            raise ValueError(f"Unsupported format {d['header']['format']}")

        if "major_version" not in d["header"]:
            raise ValueError("No major_version in JSON file, "
                             "unable to determine the format of the json file.")

        if "minor_version" not in d["header"]:
            raise ValueError("No minor_version in JSON file, "
                             "unable to determine the format of the json file.")

        if d["header"]["major_version"] != PackageVersion().get_major_lib_json_version():
            raise ValueError(f"Unsupported major version {d['header']['major_version']}")

        if d["header"]["minor_version"] != PackageVersion().get_minor_lib_json_version():
            raise ValueError(f"Unsupported minor version {d['header']['minor_version']}")

        if "molecular_system" in d:
            from lammpsinputbuilder.loader.typedmolecule_loader import TypedMolecularSystemLoader

            loader = TypedMolecularSystemLoader()
            self.molecule = loader.dict_to_typed_molecular_system(d["molecular_system"])

        if "sections" in d:
            from lammpsinputbuilder.loader.section_loader import SectionLoader
            loader = SectionLoader()
            for s in d["sections"]:
                self.sections.append(loader.dict_to_section(s))
