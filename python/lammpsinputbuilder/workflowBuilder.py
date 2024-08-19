from lammpsinputbuilder.typedMolecule import TypedMolecule

from pathlib import Path
from uuid import uuid4
import logging
import tempfile

logger = logging.getLogger(__name__)

class WorkflowBuilder:

    def __init__(self):
        self.molecule = None
        self.sections =[]

    def setTypedMolecule(self, molecule: TypedMolecule):
        self.molecule = molecule

    def getTypedMolecule(self) -> TypedMolecule:
        return self.molecule
    
    def generateInputs(self, jobFolderPrefix: Path = None) -> Path:

        if self.molecule is None:
            raise ValueError("A molecule must be set before generating the input files. See setTypedMolecule().")
        
        jobID = str(uuid4())

        prefix = jobFolderPrefix
        if prefix is None:
            prefix = Path(tempfile.gettempdir())

        jobFolder = prefix / jobID
        jobFolder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"WorkflowBuilder generated the job folder: {jobFolder}")

        # Write the initial Lammps files
        molecule = self.molecule.generateLammpsDataFile(jobFolder)
        inputPath = self.molecule.generateLammpsInputFile(jobFolder, molecule)

        # System is now declared, we can add sections to the input file

        return jobFolder