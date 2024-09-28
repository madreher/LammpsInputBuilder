"""Module containing the TypedMolecularSystem class."""

from typing import List
from pathlib import Path
import shutil
import tempfile

from ase import Atoms
from ase.io import read as ase_read
from ase.io.lammpsrun import read_lammps_dump_text as ase_read_lammps_dump_text

from lammpsinputbuilder.types import Forcefield, BoundingBoxStyle, MoleculeFileFormat, \
    GlobalInformation, ElectrostaticMethod, get_molecule_file_format_from_extension, \
    get_extension_from_molecule_file_format, get_forcefield_from_extension
from lammpsinputbuilder.utility.model_to_data import molecule_to_lammps_data_pbc, \
    molecule_to_lammps_input
from lammpsinputbuilder.quantities import LammpsUnitSystem


class TypedMolecularSystem:
    """
    Handler for a molecular system with a forcefield assigned to it. This class is responsible
    for generating a LAMMPS data file for the system as well as the correspinding start of the
    input file. This class defines the interface for types molecular system and must be inherited
    for each type of forcefield.
    """

    def __init__(self, forcefield: Forcefield, bbox_style: BoundingBoxStyle):
        self.ff_type = forcefield
        self.bbox_style = bbox_style

    def get_forcefield_type(self) -> Forcefield:
        return self.ff_type

    def get_boundingbox_style(self) -> BoundingBoxStyle:
        return self.bbox_style

    def set_forcefield_type(self, ff_type: Forcefield):
        self.ff_type = ff_type

    def get_unit_system(self) -> LammpsUnitSystem:
        if self.get_forcefield_type() == Forcefield.REAX:
            return LammpsUnitSystem.REAL
        if self.get_forcefield_type() in [Forcefield.AIREBO, Forcefield.AIREBOM, Forcefield.REBO]:
            return LammpsUnitSystem.METAL

        raise ValueError(
            f"Unit system unknown for the forcefield type {self.get_forcefield_type()}.")

    def set_boundingbox_style(self, bbox_style: BoundingBoxStyle):
        self.bbox_style = bbox_style

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["forcefield"] = self.get_forcefield_type().value
        result["bbox_style"] = self.get_boundingbox_style().value
        return result

    def from_dict(self, d: dict, version: int):
        # We're not checking the class name here, it's up to the inheriting
        # class
        del version  # unused
        self.set_forcefield_type(Forcefield(d["forcefield"]))
        self.set_boundingbox_style(BoundingBoxStyle(d["bbox_style"]))

    def get_default_thermo_variables(self) -> List[str]:
        return []

    def generate_lammps_data_file(self, job_folder: Path) -> GlobalInformation:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def generate_lammps_input_file(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def get_lammps_data_filename(self) -> str:
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")


class ReaxTypedMolecularSystem(TypedMolecularSystem):
    """
    Handler for a molecular system with a Reax forcefield assigned to it. 
    This class is responsible for generating a LAMMPS data file for the 
    system as well as the correspinding start of the input file.
    """

    def __init__(
            self,
            bbox_style: BoundingBoxStyle = BoundingBoxStyle.PERIODIC,
            electrostatic_method: ElectrostaticMethod = ElectrostaticMethod.QEQ):
        super().__init__(Forcefield.REAX, bbox_style)
        self.electrostatic_method = electrostatic_method

        self.model_loaded = False
        self.molecule_content = ""
        self.forcefield_content = ""
        self.forcefield_path = None
        self.molecule_path = None
        self.molecule_format = None
        self.atoms = None

    def get_unit_system(self) -> LammpsUnitSystem:
        return LammpsUnitSystem.REAL

    def load_from_file(
            self,
            molecule_path: Path,
            forcefield_path: Path,
            format_hint: MoleculeFileFormat = None):
        # Check for file exist
        if not forcefield_path.is_file():
            raise FileNotFoundError(f"File {forcefield_path} not found.")
        if not molecule_path.is_file():
            raise FileNotFoundError(f"File {molecule_path} not found.")

        # Check for supported molecule format
        self.molecule_format = get_molecule_file_format_from_extension(
            molecule_path.suffix)

        # Check for supported forcefield format
        forcefield_format = get_forcefield_from_extension(forcefield_path.suffix)
        if forcefield_format != Forcefield.REAX:
            raise ValueError(
                f"Forcefield file {forcefield_path} is not a Reax forcefield, \
                expecting .reax extension.")

        # Set paths
        self.molecule_path = molecule_path
        self.forcefield_path = forcefield_path

        # Read molecule
        with open(self.molecule_path, "r", encoding="utf-8") as f:
            self.molecule_content = f.read()
            if format_hint is not None:
                self.molecule_format = format_hint
            elif self.molecule_path.suffix.lower() == ".xyz":
                self.molecule_format = MoleculeFileFormat.XYZ
            elif self.molecule_path.suffix.lower() == ".mol2":
                self.molecule_format = MoleculeFileFormat.MOL2
            elif self.molecule_path.suffix.lower() == ".lammpstrj":
                self.molecule_format = MoleculeFileFormat.LAMMPS_DUMP_TEXT
            else:  # Should never happen with after the format check above
                raise NotImplementedError(
                    f"Molecule format {self.molecule_path.suffix} not supported.")

        # Read forcefield
        with open(self.forcefield_path, "r", encoding="utf-8") as f:
            self.forcefield_content = f.read()

        if self.molecule_format == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
            with open(self.molecule_path, "r", encoding="utf-8") as f:
                self.atoms = ase_read_lammps_dump_text(f)
        else:
            self.atoms = ase_read(self.molecule_path)

        self.model_loaded = True

    def load_from_string(
            self,
            molecule_content: str,
            molecule_format: MoleculeFileFormat,
            forcefield_content: str,
            forcefield_file_name: Path,
            molecule_file_name: str = Path):

        if forcefield_file_name.suffix.lower() != ".reax":
            raise ValueError(
                f"Forcefield file {forcefield_file_name} is not a Reax forcefield, \
                expecting .reax extension.")

        self.molecule_content = molecule_content
        self.molecule_format = molecule_format
        if molecule_file_name != "":
            self.molecule_path = Path(molecule_file_name)
        else:
            self.molecule_path = Path(
                "model." + get_extension_from_molecule_file_format(molecule_format))

        self.forcefield_content = forcefield_content
        self.forcefield_path = Path(forcefield_file_name)

        # Create a temporary file to be read by ase
        job_folder = Path(tempfile.mkdtemp())
        model_path = job_folder / \
            Path("model." + get_extension_from_molecule_file_format(molecule_format))

        with open(model_path, "w", encoding="utf-8") as f:
            f.write(molecule_content)

        self.atoms = ase_read(model_path)

        # Remove temporary folder
        shutil.rmtree(job_folder)

        self.model_loaded = True

    def is_model_loaded(self) -> bool:
        return self.model_loaded

    def get_ase_model(self) -> Atoms:
        if not self.is_model_loaded():
            raise ValueError(
                "Model is not loaded, unable to return ASE atoms.")
        return self.atoms

    def get_molecule_content(self) -> str:
        return self.molecule_content

    def get_molecule_format(self) -> MoleculeFileFormat:
        return self.molecule_format

    def get_molecule_path(self) -> Path:
        return self.molecule_path

    def get_forcefield_content(self) -> str:
        return self.forcefield_content

    def get_forcefield_path(self) -> Path:
        return self.forcefield_path

    def get_electrostatic_method(self) -> ElectrostaticMethod:
        return self.electrostatic_method

    def set_electrostatic_method(self, electrostatic_method: ElectrostaticMethod):
        self.electrostatic_method = electrostatic_method

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["electrostatic_method"] = self.electrostatic_method.value
        result["is_model_loaded"] = self.model_loaded
        result["forcefield_path"] = Path(str(self.forcefield_path))
        result["molecule_path"] = Path(str(self.molecule_path))
        result["molecule_format"] = self.molecule_format.value
        result["forcefield_content"] = self.forcefield_content
        result["molecule_content"] = self.molecule_content
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        molecule_type = d["class"]
        if molecule_type != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {molecule_type}.")
        super().from_dict(d, version=version)
        self.electrostatic_method = ElectrostaticMethod(
            d["electrostatic_method"])
        self.model_loaded = d["is_model_loaded"]
        self.forcefield_path = Path(d["forcefield_path"])
        self.molecule_path = Path(d["molecule_path"])
        self.molecule_format = MoleculeFileFormat(d["molecule_format"])
        self.forcefield_content = d["forcefield_content"]
        self.molecule_content = d["molecule_content"]

    def generate_lammps_data_file(self, job_folder: Path) -> GlobalInformation:
        # TODO: Adjust code to handle the different bbox styles
        global_info = molecule_to_lammps_data_pbc(
            self.molecule_content,
            self.molecule_format,
            job_folder,
            self.get_lammps_data_filename())

        # Copy the forcefield to the job folder
        forcefield_path = job_folder / self.forcefield_path.name
        with open(forcefield_path, 'w', encoding="utf-8") as f:
            f.write(self.forcefield_content)

        return global_info

    def generate_lammps_input_file(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        return molecule_to_lammps_input(
            "lammps.input",
            job_folder /
            self.get_lammps_data_filename(),
            job_folder,
            Forcefield.REAX,
            self.forcefield_path.name,
            global_information,
            electrostatic_method=self.electrostatic_method)

    def get_lammps_data_filename(self) -> str:
        return "model.data"

    def get_default_thermo_variables(self) -> List[str]:
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
