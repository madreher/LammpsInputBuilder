from typing import List 
from pathlib import Path
from ase import Atoms
from ase.io import read as ase_read
from ase.io.lammpsrun import read_lammps_dump_text as ase_read_lammps_dump_text
import shutil
import tempfile

from lammpsinputbuilder.types import Forcefield, BoundingBoxStyle, MoleculeFileFormat, MoleculeHolder, ElectrostaticMethod, getMoleculeFileFormatFromExtension, getExtensionFromMoleculeFileFormat, getForcefieldFromExtension
from lammpsinputbuilder.utility.modelToData import moleculeToLammpsDataPBC, moleculeToLammpsInput
from lammpsinputbuilder.quantities import LammpsUnitSystem

class TypedMolecule:
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
            raise ValueError(f"Unit system unknown for the forcefield type {self.getForcefieldType()}.")

    def setBoundingBoxStyle(self, bboxStyle: BoundingBoxStyle):
        self.bboxStyle = bboxStyle

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["forcefield"] = self.getForcefieldType().value
        result["bboxStyle"] = self.getBoundingBoxStyle().value
        return result
    
    def fromDict(self, d: dict, version: int):
        # We're not checking the class name here, it's up to the inheriting class
        self.setForcefieldType(Forcefield(d["forcefield"]))
        self.setBoundingBoxStyle(BoundingBoxStyle(d["bboxStyle"]))
    
    def getDefaultThermoVariables(self) -> List[str]:
        return []
    
    def getUnitsystem(self) -> LammpsUnitSystem:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
    def generateLammpsDataFile(self, jobFolder:Path) -> MoleculeHolder:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
    def generateLammpsInputFile(self, jobFolder:Path, molecule: MoleculeHolder) -> Path:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
    def getLammpsDataFileName(self) -> str:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    

class ReaxTypedMolecule(TypedMolecule):
    """
    Handler for a molecular system with a Reax forcefield assigned to it. This class is responsible for 
    generating a LAMMPS data file for the system as well as the correspinding start of the input file.
    """
    def __init__(self, bboxStyle: BoundingBoxStyle = BoundingBoxStyle.PERIODIC, electrostaticMethod: ElectrostaticMethod = ElectrostaticMethod.QEQ):
        super().__init__(Forcefield.REAX, bboxStyle)
        self.electrostaticMethod = electrostaticMethod

        self.modelLoaded = False
        self.moleculeContent = ""
        self.forcefieldContent = ""
        self.forcefieldPath = None
        self.moleculePath = None
        self.moleculeFormat = None
        self.atoms = None

    def getUnitsystem(self) -> LammpsUnitSystem:
        return LammpsUnitSystem.REAL

    def loadFromFile(self, moleculePath: Path, forcefieldPath: Path, formatHint: MoleculeFileFormat = None):
        # Check for file exist
        if not forcefieldPath.is_file():
            raise FileNotFoundError(f"File {forcefieldPath} not found.")
        if not moleculePath.is_file():
            raise FileNotFoundError(f"File {moleculePath} not found.")
        
        # Check for supported molecule format
        self.moleculeFormat = getMoleculeFileFormatFromExtension(moleculePath.suffix)

        # Check for supported forcefield format
        forcefieldFormat = getForcefieldFromExtension(forcefieldPath.suffix)
        if forcefieldFormat != Forcefield.REAX:
            raise ValueError(f"Forcefield file {forcefieldPath} is not a Reax forcefield, expecting .reax extension.")
        
        # Set paths
        self.moleculePath = moleculePath
        self.forcefieldPath = forcefieldPath

        # Read molecule
        with open(self.moleculePath, "r") as f:
            self.moleculeContent = f.read()
            if formatHint is not None:
                self.moleculeFormat = formatHint
            elif self.moleculePath.suffix.lower() == ".xyz":
                self.moleculeFormat = MoleculeFileFormat.XYZ
            elif self.moleculePath.suffix.lower() == ".mol2":
                self.moleculeFormat = MoleculeFileFormat.MOL2
            elif self.moleculePath.suffix.lower() == ".lammpstrj":
                self.moleculeFormat = MoleculeFileFormat.LAMMPS_DUMP_TEXT
            else: # Should never happen with after the format check above
                raise NotImplementedError(f"Molecule format {self.moleculePath.suffix} not supported.")
        
        # Read forcefield
        with open(self.forcefieldPath, "r") as f:
            self.forcefieldContent = f.read()

        if self.moleculeFormat == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
            with open(self.moleculePath, "r") as f:
                self.atoms = ase_read_lammps_dump_text(f)
        else:
            self.atoms = ase_read(self.moleculePath)

        self.modelLoaded = True

    def loadFromStrings(self, moleculeContent: str, moleculeFormat: MoleculeFileFormat, forcefieldContent: str, forcefieldFileName:Path, moleculeFileName:str = Path):
        
        if forcefieldFileName.suffix.lower() != ".reax":
            raise ValueError(f"Forcefield file {forcefieldFileName} is not a Reax forcefield, expecting .reax extension.")

        self.moleculeContent = moleculeContent
        self.moleculeFormat = moleculeFormat
        if moleculeFileName != "":
            self.moleculePath = Path(moleculeFileName)
        else:
            self.moleculePath = Path("model." + getExtensionFromMoleculeFileFormat(moleculeFormat))

        self.forcefieldContent = forcefieldContent
        self.forcefieldPath = Path(forcefieldFileName)
        
        # Create a temporary file to be read by ase
        jobFolder = Path(tempfile.mkdtemp())
        modelPath = jobFolder / Path("model." + getExtensionFromMoleculeFileFormat(moleculeFormat))

        with open(modelPath, "w") as f:
            f.write(moleculeContent)

        self.atoms = ase_read(modelPath)

        # Remove temporary folder
        shutil.rmtree(jobFolder)

        self.modelLoaded = True

    def isModelLoaded(self) -> bool:
        return self.modelLoaded
    
    def getASEAtoms(self) -> Atoms:
        if not self.isModelLoaded():
            raise ValueError("Model is not loaded, unable to return ASE atoms.")
        return self.atoms
    
    def getMoleculeContent(self) -> str:
        return self.moleculeContent
    
    def getMoleculeFormat(self) -> MoleculeFileFormat:
        return self.moleculeFormat
    
    def getMoleculePath(self) -> Path:
        return self.moleculePath
    
    def getForcefieldContent(self) -> str:
        return self.forcefieldContent
    
    def getForcefieldPath(self) -> Path:
        return self.forcefieldPath
    
    def getElectrostaticMethod(self) -> ElectrostaticMethod:
        return self.electrostaticMethod
    
    def setElectrostaticMethod(self, electrostaticMethod: ElectrostaticMethod):
        self.electrostaticMethod = electrostaticMethod

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["electrostaticMethod"] = self.electrostaticMethod.value
        result["isModelLoaded"] = self.modelLoaded
        result["forcefieldPath"] = Path(str(self.forcefieldPath))
        result["moleculePath"] = Path(str(self.moleculePath))
        result["moleculeFormat"] = self.moleculeFormat.value
        result["forcefieldContent"] = self.forcefieldContent
        result["moleculeContent"] = self.moleculeContent
        return result
    
    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        moleculeType = d["class"]
        if moleculeType != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {moleculeType}.")
        super().fromDict(d, version=version)
        self.electrostaticMethod = ElectrostaticMethod(d["electrostaticMethod"])
        self.modelLoaded = d["isModelLoaded"]
        self.forcefieldPath = Path(d["forcefieldPath"])
        self.moleculePath = Path(d["moleculePath"])
        self.moleculeFormat = MoleculeFileFormat(d["moleculeFormat"])
        self.forcefieldContent = d["forcefieldContent"]
        self.moleculeContent = d["moleculeContent"]
        
        
    def generateLammpsDataFile(self, jobFolder:Path) -> MoleculeHolder:
        # TODO: Adjust code to handle the different bbox styles
        molecule = moleculeToLammpsDataPBC(self.moleculeContent, self.moleculeFormat, jobFolder, self.getLammpsDataFileName())

        # Copy the forcefield to the job folder
        forcefieldPath = jobFolder / self.forcefieldPath.name
        with open(forcefieldPath, 'w') as f:
            f.write(self.forcefieldContent)

        return molecule
    
    def generateLammpsInputFile(self, jobFolder:Path, molecule: MoleculeHolder) -> Path:
        return moleculeToLammpsInput("lammps.input", jobFolder / self.getLammpsDataFileName(), jobFolder, Forcefield.REAX, self.forcefieldPath.name, molecule, electrostaticMethod=self.electrostaticMethod)
    
    def getLammpsDataFileName(self) -> str:
        return "model.data"
    
    def getDefaultThermoVariables(self) -> List[str]:
        return ['step', 'v_eb', 'v_ea', 'v_elp', 'v_emol', 'v_ev', 'v_epen', 'v_ecoa', 'v_ehb', 'v_et', 'v_eco', 'v_ew', 'v_ep', 'v_efi', 'v_eqeq']
    
