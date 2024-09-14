from enum import Enum
from typing import List 
from ase import Atoms

class Forcefield(Enum):
    REAX = 1,
    AIREBO = 2,
    REBO = 3,
    AIREBOM = 4

def getForcefieldFromExtension(extension: str) -> Forcefield:
    if extension.lower() == ".reax":
        return Forcefield.REAX
    elif extension.lower() == ".airebo":
        return Forcefield.AIREBO
    elif extension.lower() == ".rebo":
        return Forcefield.REBO
    elif extension.lower() == ".airebo-m":
        return Forcefield.AIREBOM
    else:
        raise NotImplementedError(f"Forcefield {extension} not supported.")
    
def getExtensionFromForcefield(forcefield: Forcefield) -> str:
    if forcefield == Forcefield.REAX:
        return ".reax"
    elif forcefield == Forcefield.AIREBO:
        return ".airebo"
    elif forcefield == Forcefield.REBO:
        return ".rebo"
    elif forcefield == Forcefield.AIREBOM:
        return ".airebo-m"
    else:
        raise NotImplementedError(f"Forcefield {forcefield} not supported.")

class BoundingBoxStyle(Enum):
    PERIODIC = 1,
    SHRINK = 2

class MoleculeFileFormat(Enum):
    XYZ = 1,
    MOL2 = 2, 
    LAMMPS_DUMP_TEXT = 3

def getMoleculeFileFormatFromExtension(extension: str) -> MoleculeFileFormat:
    if extension.lower() == ".xyz":
        return MoleculeFileFormat.XYZ
    elif extension.lower() == ".mol2":
        return MoleculeFileFormat.MOL2
    elif extension.lower() == ".lammpstrj":
        return MoleculeFileFormat.LAMMPS_DUMP_TEXT
    else:
        raise NotImplementedError(f"Molecule format {extension} not supported.")
    
def getExtensionFromMoleculeFileFormat(moleculeFileFormat: MoleculeFileFormat) -> str:
    if moleculeFileFormat == MoleculeFileFormat.XYZ:
        return ".xyz"
    elif moleculeFileFormat == MoleculeFileFormat.MOL2:
        return ".mol2"
    else:
        raise NotImplementedError(f"Molecule format {moleculeFileFormat} not supported.")

class ElectrostaticMethod(Enum):
    ACKS2 = 1,
    QEQ = 2

class MoleculeHolder():
    """
    Class used to store the molecule information
    """
    def __init__(self, atoms: Atoms, bboxCoords: List) -> None:
        self.atoms = atoms
        if len(bboxCoords) != 6:
            raise ValueError("Invalid number of bounding box coordinates (6 expected, received " + str(len(bboxCoords)) + ")")
        self.bboxCoords = bboxCoords
        self.bboxDims = [bboxCoords[1] - bboxCoords[0], bboxCoords[3] - bboxCoords[2], bboxCoords[5] - bboxCoords[4]]

    def getAtoms(self) -> Atoms:
        return self.atoms

    def getBboxCoords(self) -> List:
        return self.bboxCoords

    def getBboxDims(self) -> List:
        return self.bboxDims