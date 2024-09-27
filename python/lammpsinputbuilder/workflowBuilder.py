from lammpsinputbuilder.typedMolecule import TypedMolecularSystem
from lammpsinputbuilder.section import Section

from pathlib import Path
from uuid import uuid4
import shutil
import logging
import tempfile

logger = logging.getLogger(__name__)


class WorkflowBuilder:

    def __init__(self):
        self.molecule = None
        self.sections = []

    def setTypedMolecularSystem(self, molecule: TypedMolecularSystem):
        if not molecule.isModelLoaded():
            raise ValueError(
                "The molecule must be loaded before it can be set.")
        self.molecule = molecule

    def getTypedMolecularSystem(self) -> TypedMolecularSystem:
        return self.molecule

    def addSection(self, section: Section):
        self.sections.append(section)

    def generateInputs(self, jobFolderPrefix: Path = None) -> Path:

        if self.molecule is None:
            raise ValueError(
                "A molecule must be set before generating the input files. See setTypedMolecularSystem().")

        jobID = str(uuid4())

        prefix = jobFolderPrefix
        if prefix is None:
            prefix = Path(tempfile.gettempdir())

        jobFolder = prefix / jobID
        jobFolder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"WorkflowBuilder generated the job folder: {jobFolder}")

        # Write the initial Lammps files
        globalInformation = self.molecule.generateLammpsDataFile(jobFolder)
        inputPath = self.molecule.generateLammpsInputFile(
            jobFolder, globalInformation)

        # System is now declared, we can add sections to the input file

        # First, we are going to copy the initial input file to a new file
        # This is to preserve the input file with the system declaration only
        # to help with debugging or additional manual analysis from the user
        workflowInputPath = jobFolder / "workflow.input"
        shutil.copy(inputPath, workflowInputPath)

        # Now we can add the sections
        sectionContent = ""
        for section in self.sections:
            sectionContent += section.addAllCommands(globalInformation)

        with open(workflowInputPath, "a") as f:
            f.write(sectionContent)

        return jobFolder
