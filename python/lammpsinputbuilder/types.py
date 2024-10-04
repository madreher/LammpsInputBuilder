"""Module containing types for lammpsinputbuilder."""

from enum import IntEnum
from typing import List
from ase import Atoms
from lammpsinputbuilder.quantities import LammpsUnitSystem


class Forcefield(IntEnum):
    REAX = 1
    AIREBO = 2
    REBO = 3
    AIREBOM = 4


def get_forcefield_from_extension(extension: str) -> Forcefield:
    if extension.lower() == ".reax":
        return Forcefield.REAX
    if extension.lower() == ".airebo":
        return Forcefield.AIREBO
    if extension.lower() == ".rebo":
        return Forcefield.REBO
    if extension.lower() == ".airebo-m":
        return Forcefield.AIREBOM

    raise NotImplementedError(f"Forcefield {extension} not supported.")


def get_extension_from_forcefield(forcefield: Forcefield) -> str:
    if forcefield == Forcefield.REAX:
        return ".reax"
    if forcefield == Forcefield.AIREBO:
        return ".airebo"
    if forcefield == Forcefield.REBO:
        return ".rebo"
    if forcefield == Forcefield.AIREBOM:
        return ".airebo-m"

    raise NotImplementedError(f"Forcefield {forcefield} not supported.")


class BoundingBoxStyle(IntEnum):
    PERIODIC = 1
    SHRINK = 2


class MoleculeFileFormat(IntEnum):
    XYZ = 1
    MOL2 = 2
    LAMMPS_DUMP_TEXT = 3


def get_molecule_file_format_from_extension(extension: str) -> MoleculeFileFormat:
    if extension.lower() == ".xyz":
        return MoleculeFileFormat.XYZ
    if extension.lower() == ".mol2":
        return MoleculeFileFormat.MOL2
    if extension.lower() == ".lammpstrj":
        return MoleculeFileFormat.LAMMPS_DUMP_TEXT

    raise NotImplementedError(f"Molecule format {extension} not supported.")


def get_extension_from_molecule_file_format(
        molecule_file_format: MoleculeFileFormat) -> str:
    if molecule_file_format == MoleculeFileFormat.XYZ:
        return ".xyz"
    if molecule_file_format == MoleculeFileFormat.MOL2:
        return ".mol2"
    if molecule_file_format == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
        return ".lammpstrj"

    raise NotImplementedError(f"Molecule format {molecule_file_format} not supported.")


class ElectrostaticMethod(IntEnum):
    ACKS2 = 1
    QEQ = 2


class GlobalInformation:
    def __init__(self) -> None:
        self.unit_style = None
        self.element_table = {}
        self.atoms = None
        self.bbox_coords = None
        self.bbox_dims = None

    def set_atoms(self, atoms: Atoms):
        self.atoms = atoms

    def get_atoms(self) -> Atoms:
        return self.atoms

    def set_bbox_coords(self, bbox_coords: List[float]):
        if len(bbox_coords) != 6:
            raise ValueError(
                "Invalid number of bounding box coordinates (6 expected, received " + 
                str(len(bbox_coords)) + ")")
        self.bbox_coords = bbox_coords
        self.bbox_dims = [
            bbox_coords[1] -
            bbox_coords[0],
            bbox_coords[3] -
            bbox_coords[2],
            bbox_coords[5] -
            bbox_coords[4]]

    def get_bbox_coords(self) -> List:
        return self.bbox_coords

    def get_bbox_dims(self) -> List:
        return self.bbox_dims

    def set_unit_style(self, unit_style: LammpsUnitSystem):
        self.unit_style = unit_style

    def get_unit_style(self) -> LammpsUnitSystem:
        return self.unit_style

    def set_element_table(self, element_table: dict):
        self.element_table = element_table

    def get_element_table(self) -> dict:
        return self.element_table
