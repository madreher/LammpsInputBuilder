"""WorkflowBuilder Module"""

from pathlib import Path
from uuid import uuid4
import shutil
import logging
import tempfile

from lammpsinputbuilder.typedMolecule import TypedMolecularSystem
from lammpsinputbuilder.section import Section

logger = logging.getLogger(__name__)


class WorkflowBuilder:

    def __init__(self):
        self.molecule = None
        self.sections = []

    def set_typed_molecular_system(self, molecule: TypedMolecularSystem):
        if not molecule.isModelLoaded():
            raise ValueError(
                "The molecule must be loaded before it can be set.")
        self.molecule = molecule

    def get_typed_molecular_system(self) -> TypedMolecularSystem:
        return self.molecule

    def add_section(self, section: Section):
        self.sections.append(section)

    def generate_inputs(self, job_folder_prefix: Path = None) -> Path:

        if self.molecule is None:
            raise ValueError(
                "A molecule must be set before generating the input files. See set_typed_molecular_system().")

        job_id = str(uuid4())

        prefix = job_folder_prefix
        if prefix is None:
            prefix = Path(tempfile.gettempdir())

        job_folder = prefix / job_id
        job_folder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"WorkflowBuilder generated the job folder: {job_folder}")

        # Write the initial Lammps files
        global_information = self.molecule.generateLammpsDataFile(job_folder)
        input_path = self.molecule.generateLammpsInputFile(
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

        with open(workflow_input_path, "a") as f:
            f.write(section_content)

        return job_folder
