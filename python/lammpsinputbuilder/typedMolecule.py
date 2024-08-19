from typing import List 
from pathlib import Path
from ase import Atoms

from lammpsinputbuilder.types import Forcefield, BoundingBoxStyle, MoleculeFileFormat, MoleculeHolder, ElectrostaticMethod
from lammpsinputbuilder.utility.modelToData import moleculeToLammpsDataPBC, moleculeToLammpsInput

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

    def setBoundingBoxStyle(self, bboxStyle: BoundingBoxStyle):
        self.bboxStyle = bboxStyle

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["forcefield"] = self.getForcefieldType().value
        result["bboxStyle"] = self.getBoundingBoxStyle().value
        return result
    
    def fromDict(self, d: dict):
        # We're not checking the class name here, it's up to the inheriting class
        self.setForcefieldType(Forcefield(d["forcefield"]))
        self.setBoundingBoxStyle(BoundingBoxStyle(d["bboxStyle"]))
    
    def getDefaultThermoVariables(self) -> List[str]:
        return []
    
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
    def __init__(self, bboxStyle: BoundingBoxStyle, forcefieldPath: Path, moleculePath: Path, electrostaticMethod: ElectrostaticMethod):
        super().__init__(Forcefield.REAX, bboxStyle)
        self.forcefieldPath = forcefieldPath
        self.moleculePath = moleculePath
        self.moleculeFormat = MoleculeFileFormat.XYZ
        self.electrostaticMethod = electrostaticMethod

        self.moleculeContent = ""
        self.forcefieldContent = ""

        # Check for file exist
        if not self.forcefieldPath.is_file():
            raise FileNotFoundError(f"File {self.forcefieldPath} not found.")
        if not self.moleculePath.is_file():
            raise FileNotFoundError(f"File {self.moleculePath} not found.")
        
        # Check for supported molecule format
        supportedMoleculeFileFormats = [".xyz", ".mol2"]
        if self.moleculePath.suffix.lower() not in supportedMoleculeFileFormats:
            raise NotImplementedError(f"Molecule format {self.moleculePath.suffix} not supported.")

        # Check for supported forcefield format
        supportedForcefieldFileFormats = [".reax"]
        if self.forcefieldPath.suffix.lower() not in supportedForcefieldFileFormats:
            raise NotImplementedError(f"Forcefield format {self.forcefieldPath.suffix} not supported.")
        
        # Read molecule
        with open(self.moleculePath, "r") as f:
            self.moleculeContent = f.read()
            if self.moleculePath.suffix.lower() == ".xyz":
                self.moleculeFormat = MoleculeFileFormat.XYZ
            elif self.moleculePath.suffix.lower() == ".mol2":
                self.moleculeFormat = MoleculeFileFormat.MOL2
        
        # Read forcefield
        with open(self.forcefieldPath, "r") as f:
            self.forcefieldContent = f.read()
        
    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["forcefieldPath"] = Path(str(self.forcefieldPath))
        result["moleculePath"] = Path(str(self.moleculePath))
        result["moleculeFormat"] = self.moleculeFormat.value
        result["forcefieldContent"] = self.forcefieldContent
        result["moleculeContent"] = self.moleculeContent
        result["electrostaticMethod"] = self.electrostaticMethod.value
        return result
    
    def fromDict(self, d: dict):
        # Make sure that we are reading the right class
        moleculeType = d["class"]
        if moleculeType != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {moleculeType}.")
        super().fromDict(d)
        self.forcefieldPath = Path(d["forcefieldPath"])
        self.moleculePath = Path(d["moleculePath"])
        self.moleculeFormat = MoleculeFileFormat(d["moleculeFormat"])
        self.forcefieldContent = d["forcefieldContent"]
        self.moleculeContent = d["moleculeContent"]
        self.electrostaticMethod = ElectrostaticMethod(d["electrostaticMethod"])
        
    def generateLammpsDataFile(self, jobFolder:Path) -> MoleculeHolder:
        # TODO: Adjust code to handle the different bbox styles
        molecule = moleculeToLammpsDataPBC(self.moleculeContent, self.moleculeFormat, jobFolder, self.getLammpsDataFileName())

        return molecule
    
    def generateLammpsInputFile(self, jobFolder:Path, molecule: MoleculeHolder) -> Path:
        moleculeToLammpsInput("lammps.input", jobFolder / self.getLammpsDataFileName(), jobFolder, Forcefield.REAX, self.forcefieldPath.name, molecule, electrostaticMethod=self.electrostaticMethod)
    
    def getLammpsDataFileName(self) -> str:
        return "model.data"
    
