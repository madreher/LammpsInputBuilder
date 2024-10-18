"""Module containing types for lammpsinputbuilder."""

from enum import IntEnum
from typing import List
from ase import Atoms
from lammpsinputbuilder.quantities import LammpsUnitSystem


class Forcefield(IntEnum):
    """
    Enumeration for the supported forcefields types
    """
    REAX = 1
    AIREBO = 2
    REBO = 3
    AIREBOM = 4


def get_forcefield_from_extension(extension: str) -> Forcefield:
    """
    Get the forcefield type enum from a file extension. 
    The file extension must be of the form ".<extension>"

    Args:
        extension (str): The file extension

    Returns:
        Forcefield: The forcefield type enum

    Raises:
        NotImplementedError: If the forcefield type is not supported
    """
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
    """
    Get the file extension from a forcefield type enum. 

    Args:
        forcefield (Forcefield): The forcefield type enum

    Returns:
        str: The file extension

    Raises:
        NotImplementedError: If the forcefield type is not supported
    """
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
    """
    Enumeration for the supported bounding box styles
    """
    PERIODIC = 1
    SHRINK = 2


class MoleculeFileFormat(IntEnum):
    """
    Enumeration for the supported molecule file formats
    """
    XYZ = 1
    MOL2 = 2
    LAMMPS_DUMP_TEXT = 3


def get_molecule_file_format_from_extension(extension: str) -> MoleculeFileFormat:
    """
    Get the molecule file format enum from a file extension. 
    The file extension must be of the form ".<extension>".
    The given extension is lowercased before being compared.

    Args:
        extension (str): The file extension

    Returns:
        MoleculeFileFormat: The molecule file format enum

    Raises:
        NotImplementedError: If the molecule file format is not supported
    """
    if extension.lower() == ".xyz":
        return MoleculeFileFormat.XYZ
    if extension.lower() == ".mol2":
        return MoleculeFileFormat.MOL2
    if extension.lower() == ".lammpstrj":
        return MoleculeFileFormat.LAMMPS_DUMP_TEXT

    raise NotImplementedError(f"Molecule format {extension} not supported.")


def get_extension_from_molecule_file_format(
        molecule_file_format: MoleculeFileFormat) -> str:
    """
    Get the file extension from a molecule file format enum. 

    Args:
        molecule_file_format (MoleculeFileFormat): The molecule file format enum

    Returns:
        str: The file extension

    Raises:
        NotImplementedError: If the molecule file format is not supported
    """
    if molecule_file_format == MoleculeFileFormat.XYZ:
        return ".xyz"
    if molecule_file_format == MoleculeFileFormat.MOL2:
        return ".mol2"
    if molecule_file_format == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
        return ".lammpstrj"

    raise NotImplementedError(f"Molecule format {molecule_file_format} not supported.")


class ElectrostaticMethod(IntEnum):
    """
    Enumeration for the supported electrostatic methods
    """
    ACKS2 = 1
    QEQ = 2


class GlobalInformation:
    """
    Class used as a container for global information related to the molecular 
    system and workflow which can be used by several LIB objects like Extensions, etc 
    to adjust their output of Lammps commmands. A GlobalInformation object is always 
    generated when starting to convert a workflow into Lammps commands and is forwarded 
    to all the LIB objects in the workflow when traversing the workflow graph.
    """
    def __init__(self) -> None:
        self.unit_style = None
        self.element_table = {}
        self.atoms = None
        self.bbox_coords = None
        self.bbox_dims = None

    def set_atoms(self, atoms: Atoms):
        """
        Set the atoms object from loading a ASE model.
        Args:
            atoms (Atoms): The atoms object
        """
        self.atoms = atoms

    def get_atoms(self) -> Atoms:
        """
        Get the atoms object produced by ASE
        Returns:
            Atoms: The atoms object
        """
        return self.atoms

    def set_bbox_coords(self, bbox_coords: List[float]):
        """
        Set the bounding box coordinates. The format is [x0, x1, y0, y1, z0, z1]
        where x0 is the minimum x value, x1 is the maximum x value, etc.
        The dimentions are calculated as x1-x0, y1-y0, etc.

        Args:
            bbox_coords (List[float]): The bounding box coordinates
        """
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
        """
        Get the bounding box coordinates. The coordinates are [x0, x1, y0, y1, z0, z1]
        where x0 is the minimum x value, x1 is the maximum x value, etc.
        Returns:
            List[float]: The bounding box coordinates
        """
        return self.bbox_coords

    def get_bbox_dims(self) -> List:
        """
        Get the bounding box dimensions. The dimensions are [x,y,z] calculated as x1-x0, y1-y0, etc.
        Returns:
            List[float]: The bounding box dimensions
        """
        return self.bbox_dims

    def set_unit_style(self, unit_style: LammpsUnitSystem):
        """
        Declare the unit style of the molecular system
        Args:
            unit_style (LammpsUnitSystem): The unit style
        """
        self.unit_style = unit_style

    def get_unit_style(self) -> LammpsUnitSystem:
        """
        Get the unit style of the molecular system
        Returns:
            LammpsUnitSystem: The unit style
        """
        return self.unit_style

    def set_element_table(self, element_table: dict):
        """
        Map a lammps type to an element name. The map must have the form 
        {lammps_type: element_name}.
        This table only makes sense in the content of a Lammps data file
        declaring atom types.
        Args:
            element_table (dict): The element table
        """
        self.element_table = element_table

    def get_element_table(self) -> dict:
        """
        Get the element table
        Returns:
            dict: The element table
        """
        return self.element_table
