from enum import Enum
from typing import List 
from ase import Atoms

class Forcefield(Enum):
    REAX = 1,
    AIREBO = 2,
    REBO = 3,
    AIREBOM = 4

class BoundingBoxStyle(Enum):
    PERIODIC = 1,
    SHRINK = 2

class MoleculeFileFormat(Enum):
    XYZ = 1,
    MOL2 = 2

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
            raise ValueError("Invalid number of bounding box coordinates")
        self.bboxCoords = bboxCoords
        self.bboxDims = [bboxCoords[1] - bboxCoords[0], bboxCoords[3] - bboxCoords[2], bboxCoords[5] - bboxCoords[4]]

    def getAtoms(self) -> Atoms:
        return self.atoms

    def getBboxCoords(self) -> List:
        return self.bboxCoords

    def getBboxDims(self) -> List:
        return self.bboxDims