"""Module containing types for lammpsinputbuilder."""

from enum import Enum
from typing import List
from ase import Atoms
from lammpsinputbuilder.quantities import LammpsUnitSystem


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
        raise NotImplementedError(
            f"Molecule format {extension} not supported.")


def getExtensionFromMoleculeFileFormat(
        molecule_file_format: MoleculeFileFormat) -> str:
    if molecule_file_format == MoleculeFileFormat.XYZ:
        return ".xyz"
    elif molecule_file_format == MoleculeFileFormat.MOL2:
        return ".mol2"
    else:
        raise NotImplementedError(
            f"Molecule format {molecule_file_format} not supported.")


class ElectrostaticMethod(Enum):
    ACKS2 = 1,
    QEQ = 2


class MoleculeHolder():
    """
    Class used to store the molecule information
    """

    def __init__(self, atoms: Atoms, bbox_coords: List) -> None:
        self.atoms = atoms
        if len(bbox_coords) != 6:
            raise ValueError(
                "Invalid number of bounding box coordinates (6 expected, received " + str(len(bbox_coords)) + ")")
        self.bbox_coords = bbox_coords
        self.bboxDims = [
            bbox_coords[1] -
            bbox_coords[0],
            bbox_coords[3] -
            bbox_coords[2],
            bbox_coords[5] -
            bbox_coords[4]]

    def getAtoms(self) -> Atoms:
        return self.atoms

    def getBboxCoords(self) -> List:
        return self.bbox_coords

    def getBboxDims(self) -> List:
        return self.bboxDims


class GlobalInformation:
    def __init__(self) -> None:
        self.unitStyle = None
        self.elementTable = {}
        self.atoms = None
        self.bbox_coords = None
        self.bboxDims = None

    def setAtoms(self, atoms: Atoms):
        self.atoms = atoms

    def getAtoms(self) -> Atoms:
        return self.atoms

    def setBBoxCoords(self, bbox_coords: List):
        if len(bbox_coords) != 6:
            raise ValueError(
                "Invalid number of bounding box coordinates (6 expected, received " + str(len(bbox_coords)) + ")")
        self.bbox_coords = bbox_coords
        self.bboxDims = [
            bbox_coords[1] -
            bbox_coords[0],
            bbox_coords[3] -
            bbox_coords[2],
            bbox_coords[5] -
            bbox_coords[4]]

    def getBBoxCoords(self) -> List:
        return self.bbox_coords

    def getBboxDims(self) -> List:
        return self.bboxDims

    def setUnitStyle(self, unitStyle: LammpsUnitSystem):
        self.unitStyle = unitStyle

    def getUnitStyle(self) -> LammpsUnitSystem:
        return self.unitStyle

    def setElementTable(self, elementTable: dict):
        self.elementTable = elementTable

    def getElementTable(self) -> dict:
        return self.elementTable
