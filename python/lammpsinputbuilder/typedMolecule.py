"""Module containing the TypedMolecularSystem class."""

from typing import List
from pathlib import Path
import shutil
import tempfile

from ase import Atoms
from ase.io import read as ase_read
from ase.io.lammpsrun import read_lammps_dump_text as ase_read_lammps_dump_text

from lammpsinputbuilder.types import Forcefield, BoundingBoxStyle, MoleculeFileFormat, GlobalInformation, ElectrostaticMethod, get_molecule_file_format_from_extension, get_extension_from_molecule_file_format, get_forcefield_from_extension
from lammpsinputbuilder.utility.modelToData import molecule_to_lammps_data_pbc, molecule_to_lammps_input
from lammpsinputbuilder.quantities import LammpsUnitSystem


class TypedMolecularSystem:
    """
    Handler for a molecular system with a forcefield assigned to it. This class is responsible for
    generating a LAMMPS data file for the system as well as the correspinding start of the input file.
    This class defines the interface for types molecular system and must be inherited for each type of forcefield.
    """

    def __init__(self, forcefield: Forcefield, bboxStyle: BoundingBoxStyle):
        self.ffType = forcefield
        self.bboxStyle = bboxStyle

    def getForcefieldType(self) -> Forcefield:
        return self.ffType

    def getBoundingBoxStyle(self) -> BoundingBoxStyle:
        return self.bboxStyle

    def setForcefieldType(self, ffType: Forcefield):
        self.ffType = ffType

    def getUnitsystem(self) -> LammpsUnitSystem:
        if self.getForcefieldType() == Forcefield.REAX:
            return LammpsUnitSystem.REAL
        elif self.getForcefieldType() in [Forcefield.AIREBO, Forcefield.AIREBOM, Forcefield.REBO]:
            return LammpsUnitSystem.METAL
        else:
            raise ValueError(
                f"Unit system unknown for the forcefield type {self.getForcefieldType()}.")

    def setBoundingBoxStyle(self, bboxStyle: BoundingBoxStyle):
        self.bboxStyle = bboxStyle

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["forcefield"] = self.getForcefieldType().value
        result["bboxStyle"] = self.getBoundingBoxStyle().value
        return result

    def from_dict(self, d: dict, version: int):
        # We're not checking the class name here, it's up to the inheriting
        # class
        self.setForcefieldType(Forcefield(d["forcefield"]))
        self.setBoundingBoxStyle(BoundingBoxStyle(d["bboxStyle"]))

    def getDefaultThermoVariables(self) -> List[str]:
        return []

    def getUnitsystem(self) -> LammpsUnitSystem:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def generateLammpsDataFile(self, job_folder: Path) -> GlobalInformation:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def generateLammpsInputFile(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def getLammpsDataFileName(self) -> str:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")


class ReaxTypedMolecularSystem(TypedMolecularSystem):
    """
    Handler for a molecular system with a Reax forcefield assigned to it. This class is responsible for
    generating a LAMMPS data file for the system as well as the correspinding start of the input file.
    """

    def __init__(
            self,
            bboxStyle: BoundingBoxStyle = BoundingBoxStyle.PERIODIC,
            electrostaticMethod: ElectrostaticMethod = ElectrostaticMethod.QEQ):
        super().__init__(Forcefield.REAX, bboxStyle)
        self.electrostaticMethod = electrostaticMethod

        self.modelLoaded = False
        self.molecule_content = ""
        self.forcefieldContent = ""
        self.forcefieldPath = None
        self.molecule_path = None
        self.moleculeFormat = None
        self.atoms = None

    def getUnitsystem(self) -> LammpsUnitSystem:
        return LammpsUnitSystem.REAL

    def loadFromFile(
            self,
            molecule_path: Path,
            forcefieldPath: Path,
            formatHint: MoleculeFileFormat = None):
        # Check for file exist
        if not forcefieldPath.is_file():
            raise FileNotFoundError(f"File {forcefieldPath} not found.")
        if not molecule_path.is_file():
            raise FileNotFoundError(f"File {molecule_path} not found.")

        # Check for supported molecule format
        self.moleculeFormat = get_molecule_file_format_from_extension(
            molecule_path.suffix)

        # Check for supported forcefield format
        forcefieldFormat = get_forcefield_from_extension(forcefieldPath.suffix)
        if forcefieldFormat != Forcefield.REAX:
            raise ValueError(
                f"Forcefield file {forcefieldPath} is not a Reax forcefield, expecting .reax extension.")

        # Set paths
        self.molecule_path = molecule_path
        self.forcefieldPath = forcefieldPath

        # Read molecule
        with open(self.molecule_path, "r") as f:
            self.molecule_content = f.read()
            if formatHint is not None:
                self.moleculeFormat = formatHint
            elif self.molecule_path.suffix.lower() == ".xyz":
                self.moleculeFormat = MoleculeFileFormat.XYZ
            elif self.molecule_path.suffix.lower() == ".mol2":
                self.moleculeFormat = MoleculeFileFormat.MOL2
            elif self.molecule_path.suffix.lower() == ".lammpstrj":
                self.moleculeFormat = MoleculeFileFormat.LAMMPS_DUMP_TEXT
            else:  # Should never happen with after the format check above
                raise NotImplementedError(
                    f"Molecule format {self.molecule_path.suffix} not supported.")

        # Read forcefield
        with open(self.forcefieldPath, "r") as f:
            self.forcefieldContent = f.read()

        if self.moleculeFormat == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
            with open(self.molecule_path, "r") as f:
                self.atoms = ase_read_lammps_dump_text(f)
        else:
            self.atoms = ase_read(self.molecule_path)

        self.modelLoaded = True

    def loadFromStrings(
            self,
            molecule_content: str,
            moleculeFormat: MoleculeFileFormat,
            forcefieldContent: str,
            forcefieldFileName: Path,
            moleculeFileName: str = Path):

        if forcefieldFileName.suffix.lower() != ".reax":
            raise ValueError(
                f"Forcefield file {forcefieldFileName} is not a Reax forcefield, expecting .reax extension.")

        self.molecule_content = molecule_content
        self.moleculeFormat = moleculeFormat
        if moleculeFileName != "":
            self.molecule_path = Path(moleculeFileName)
        else:
            self.molecule_path = Path(
                "model." + get_extension_from_molecule_file_format(moleculeFormat))

        self.forcefieldContent = forcefieldContent
        self.forcefieldPath = Path(forcefieldFileName)

        # Create a temporary file to be read by ase
        job_folder = Path(tempfile.mkdtemp())
        modelPath = job_folder / \
            Path("model." + get_extension_from_molecule_file_format(moleculeFormat))

        with open(modelPath, "w") as f:
            f.write(molecule_content)

        self.atoms = ase_read(modelPath)

        # Remove temporary folder
        shutil.rmtree(job_folder)

        self.modelLoaded = True

    def isModelLoaded(self) -> bool:
        return self.modelLoaded

    def getASEAtoms(self) -> Atoms:
        if not self.isModelLoaded():
            raise ValueError(
                "Model is not loaded, unable to return ASE atoms.")
        return self.atoms

    def getMoleculeContent(self) -> str:
        return self.molecule_content

    def getMoleculeFormat(self) -> MoleculeFileFormat:
        return self.moleculeFormat

    def getMoleculePath(self) -> Path:
        return self.molecule_path

    def getForcefieldContent(self) -> str:
        return self.forcefieldContent

    def getForcefieldPath(self) -> Path:
        return self.forcefieldPath

    def getElectrostaticMethod(self) -> ElectrostaticMethod:
        return self.electrostaticMethod

    def setElectrostaticMethod(self, electrostaticMethod: ElectrostaticMethod):
        self.electrostaticMethod = electrostaticMethod

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["electrostaticMethod"] = self.electrostaticMethod.value
        result["isModelLoaded"] = self.modelLoaded
        result["forcefieldPath"] = Path(str(self.forcefieldPath))
        result["molecule_path"] = Path(str(self.molecule_path))
        result["moleculeFormat"] = self.moleculeFormat.value
        result["forcefieldContent"] = self.forcefieldContent
        result["molecule_content"] = self.molecule_content
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        moleculeType = d["class"]
        if moleculeType != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {moleculeType}.")
        super().from_dict(d, version=version)
        self.electrostaticMethod = ElectrostaticMethod(
            d["electrostaticMethod"])
        self.modelLoaded = d["isModelLoaded"]
        self.forcefieldPath = Path(d["forcefieldPath"])
        self.molecule_path = Path(d["molecule_path"])
        self.moleculeFormat = MoleculeFileFormat(d["moleculeFormat"])
        self.forcefieldContent = d["forcefieldContent"]
        self.molecule_content = d["molecule_content"]

    def generateLammpsDataFile(self, job_folder: Path) -> GlobalInformation:
        # TODO: Adjust code to handle the different bbox styles
        globalInfo = molecule_to_lammps_data_pbc(
            self.molecule_content,
            self.moleculeFormat,
            job_folder,
            self.getLammpsDataFileName())

        # Copy the forcefield to the job folder
        forcefieldPath = job_folder / self.forcefieldPath.name
        with open(forcefieldPath, 'w') as f:
            f.write(self.forcefieldContent)

        return globalInfo

    def generateLammpsInputFile(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        return molecule_to_lammps_input(
            "lammps.input",
            job_folder /
            self.getLammpsDataFileName(),
            job_folder,
            Forcefield.REAX,
            self.forcefieldPath.name,
            global_information,
            electrostaticMethod=self.electrostaticMethod)

    def getLammpsDataFileName(self) -> str:
        return "model.data"

    def getDefaultThermoVariables(self) -> List[str]:
        return [
            'step',
            'v_eb',
            'v_ea',
            'v_elp',
            'v_emol',
            'v_ev',
            'v_epen',
            'v_ecoa',
            'v_ehb',
            'v_et',
            'v_eco',
            'v_ew',
            'v_ep',
            'v_efi',
            'v_eqeq']
