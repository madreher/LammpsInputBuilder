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
    for generating a LAMMPS data file for the system as well as the corresponding start of the
    input file. This class defines the interface for types molecular system and must be inherited
    for each type of forcefield.

    Note: 
    - This class is not meant to be used directly. Instead, use one of the subclasses dedicated 
    for a specific type of forcefield.
    - Only the period and shrink bounding box style are supported. IT is not possible to extend this 
    currently. If another type of bounding box style is needed, please submit a ticket on Github.
    """

    def __init__(self, forcefield: Forcefield, bbox_style: BoundingBoxStyle):
        """
        Constructor
        Args:
            forcefield: Forcefield type
            bbox_style: Bounding box style
        """
        self.ff_type = forcefield
        self.bbox_style = bbox_style

    def get_forcefield_type(self) -> Forcefield:
        """
        Returns the forcefield type

        Returns:
            Forcefield: type of forcefield
        """
        return self.ff_type

    def get_boundingbox_style(self) -> BoundingBoxStyle:
        """
        Returns the bounding box style

        Returns:
            BoundingBoxStyle: bounding box style
        """
        return self.bbox_style
    
    def set_boundingbox_style(self, bbox_style: BoundingBoxStyle):
        """
        Sets the bounding box style

        Args:
            bbox_style: Bounding box style
        """
        self.bbox_style = bbox_style

    def set_forcefield_type(self, ff_type: Forcefield):
        """
        Sets the forcefield type

        Args:
            ff_type: Forcefield type
        """
        self.ff_type = ff_type

    def get_unit_system(self) -> LammpsUnitSystem:
        """
        Returns the unit system

        Returns:
            LammpsUnitSystem: unit system
        """
        if self.get_forcefield_type() == Forcefield.REAX:
            return LammpsUnitSystem.REAL
        if self.get_forcefield_type() in [Forcefield.AIREBO, Forcefield.AIREBOM, Forcefield.REBO]:
            return LammpsUnitSystem.METAL

        raise ValueError(
            f"Unit system unknown for the forcefield type {self.get_forcefield_type()}.")

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the object

        Returns:
            dict: dictionary representation
        """
        result = {}
        result["class_name"] = self.__class__.__name__
        result["forcefield"] = self.get_forcefield_type().value
        result["bbox_style"] = self.get_boundingbox_style().value
        return result

    def from_dict(self, d: dict, version: int):
        """
        Loads the object from a dictionary

        Args:
            d: dictionary
            version: version of the dictionary
        """
        # We're not checking the class name here, it's up to the inheriting
        # class
        del version  # unused
        self.set_forcefield_type(Forcefield(d["forcefield"]))
        self.set_boundingbox_style(BoundingBoxStyle(d["bbox_style"]))

    def get_default_thermo_variables(self) -> List[str]:
        """
        Returns a list of default thermo variables for a particular forcefield type.

        Returns:
            List[str]: list of default thermo variables
        """
        return []

    def generate_lammps_data_file(self, job_folder: Path) -> GlobalInformation:
        """
        Generates the LAMMPS data file

        Args:
            job_folder: job folder

        Returns:
            GlobalInformation: global information
        """
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def generate_lammps_input_file(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        """
        Generates the LAMMPS input file

        Args:
            job_folder: job folder
            global_information: global information

        Returns:
            Path: path to the input file
        """
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")

    def get_lammps_data_filename(self) -> str:
        """
        Returns the name of the LAMMPS data file

        Returns:
            str: name of the LAMMPS data file
        """
        raise NotImplementedError(
            f"Method not implemented by class {__class__}")


class ReaxTypedMolecularSystem(TypedMolecularSystem):
    """
    Handler for a molecular system with a Reax forcefield assigned to it. 
    This class is responsible for generating a LAMMPS data file for the 
    system as well as the corresponding start of the input file.

    Note:
    - Only qeq and acks2 are currently supported for as electrostatic method. 
    If another method is needed, please submit a ticket on Github.

    Lammps documentation: https://docs.lammps.org/pair_reaxff.html
    """

    def __init__(
            self,
            bbox_style: BoundingBoxStyle = BoundingBoxStyle.PERIODIC,
            electrostatic_method: ElectrostaticMethod = ElectrostaticMethod.QEQ):
        """
        Constructor

        Args:
            bbox_style: Bounding box style
            electrostatic_method: Electrostatic method
        """
        super().__init__(Forcefield.REAX, bbox_style)
        self.electrostatic_method = electrostatic_method

        self.model_loaded = False
        self.molecule_content = ""
        self.forcefield_content = ""
        self.forcefield_name = None
        self.molecule_name = None
        self.molecule_format = None
        self.atoms = None

    def get_unit_system(self) -> LammpsUnitSystem:
        """
        Returns the Lammps unit system which for reax potential is always REAL

        Returns:
            LammpsUnitSystem: lammps unit system
        """
        return LammpsUnitSystem.REAL

    def load_from_file(
            self,
            molecule_path: Path,
            forcefield_path: Path,
            format_hint: MoleculeFileFormat = None):
        """
        Loads the molecule and potential files. For the molecule file, the function tries to 
        guess the format from the file extension or the format hint if provided by the user.

        Once loaded, the content of these files are stored in memory and will be written into 
        the job folder when producing the LAMMPS input files.

        Note:
        - Only mol2, xyz, and lammpstrj are currently supported via the reader from ASE. 
        If another format is needed, please submit a ticket on Github.

        Args:
            molecule_path: path to the molecule file
            forcefield_path: path to the forcefield file
            format_hint: hint for the molecule format

        Raises:
            FileNotFoundError: If the molecule or forcefield file is not found
            ValueError: If the forcefield file is not a rebo forcefield
            NotImplementedError: If the molecule format is not supported
        """
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
        self.molecule_name = Path(molecule_path.name)
        self.forcefield_name = Path(forcefield_path.name)

        # Read molecule
        with open(molecule_path, "r", encoding="utf-8") as f:
            self.molecule_content = f.read()
            if format_hint is not None:
                self.molecule_format = format_hint
            elif self.molecule_name.suffix.lower() == ".xyz":
                self.molecule_format = MoleculeFileFormat.XYZ
            elif self.molecule_name.suffix.lower() == ".mol2":
                self.molecule_format = MoleculeFileFormat.MOL2
            elif self.molecule_name.suffix.lower() == ".lammpstrj":
                self.molecule_format = MoleculeFileFormat.LAMMPS_DUMP_TEXT
            else:  # Should never happen with after the format check above
                raise NotImplementedError(
                    f"Molecule format {self.molecule_name.suffix} not supported.")

        # Read forcefield
        with open(forcefield_path, "r", encoding="utf-8") as f:
            self.forcefield_content = f.read()

        # Load the ASE Atom object
        if self.molecule_format == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
            with open(molecule_path, "r", encoding="utf-8") as f:
                self.atoms = ase_read_lammps_dump_text(f)
        else:
            self.atoms = ase_read(molecule_path)

        self.model_loaded = True

    def load_from_string(
            self,
            molecule_content: str,
            molecule_format: MoleculeFileFormat,
            forcefield_content: str,
            forcefield_file_name: Path,
            molecule_file_name: Path):
        """
        Loads the molecule and potential from strings. For both the molecule and potential content, 
        the user is responsible for providing their respective file names as well as the format in the case 
        of the molecule content.

        Once loaded, the content of these files are stored in memory and will be written into 
        the job folder when producing the LAMMPS input files.

        Note:
        - Only mol2, xyz, and lammpstrj are currently supported via the reader from ASE. 
        If another format is needed, please submit a ticket on Github.

        Args:
            molecule_content: content of the molecule file
            molecule_format: format of the molecule file
            forcefield_content: content of the forcefield file
            forcefield_file_name: name of the forcefield file
            molecule_file_name: name of the molecule file
        """

        if forcefield_file_name.suffix.lower() != ".reax":
            raise ValueError(
                f"Forcefield file {forcefield_file_name} is not a Reax forcefield, \
                expecting .reax extension.")

        self.molecule_content = molecule_content
        self.molecule_format = molecule_format
        if molecule_file_name != "":
            self.molecule_name = Path(molecule_file_name)
        else:
            self.molecule_name = Path(
                "model." + get_extension_from_molecule_file_format(molecule_format))

        self.forcefield_content = forcefield_content
        self.forcefield_name = Path(forcefield_file_name)

        # Create a temporary file to be read by ase
        # This is wasteflul, but I haven't found a way to load a molecule into ASE from a string
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
        """
        Returns whether the model is loaded or not

        Returns:
            bool: True if the model is loaded, False otherwise
        """
        return self.model_loaded

    def get_ase_model(self) -> Atoms:
        """
        Returns the ASE atoms object. If a model is not currently loaded, then returns None

        Returns:
            Atoms: ASE atoms object
        """
        return self.atoms

    def get_molecule_content(self) -> str:
        """
        Returns the molecule content. If a model is not currently loaded, then returns en empty string.

        Returns:
            str: Molecule content
        """
        return self.molecule_content

    def get_molecule_format(self) -> MoleculeFileFormat:
        """
        Returns the molecule format. If a model is not currently loaded, then returns None.

        Returns:
            MoleculeFileFormat: Molecule format
        """
        return self.molecule_format

    def get_molecule_name(self) -> Path:
        """
        Returns the molecule name. If a model is not currently loaded, then returns en empty string.

        Returns:
            Path: Molecule name
        """
        return self.molecule_name

    def get_forcefield_content(self) -> str:
        """
        Returns the forcefield content. If a model is not currently loaded, then returns en empty string.

        Returns:
            str: Forcefield content
        """
        return self.forcefield_content

    def get_forcefield_name(self) -> Path:
        """
        Returns the forcefield file name. If a model is not currently loaded, then returns en empty string.

        Returns:
            Path: Forcefield name
        """
        return self.forcefield_name

    def get_electrostatic_method(self) -> ElectrostaticMethod:
        """
        Returns the electrostatic method. 

        Returns:
            ElectrostaticMethod: Electrostatic method
        """
        return self.electrostatic_method

    def set_electrostatic_method(self, electrostatic_method: ElectrostaticMethod):
        """
        Sets the electrostatic method.

        Args:
            electrostatic_method (ElectrostaticMethod): The electrostatic method

        Returns:
            None
        """
        self.electrostatic_method = electrostatic_method

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the typed molecule

        Returns:
            dict: Dictionary representation of the typed molecule
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["electrostatic_method"] = self.electrostatic_method.value
        result["is_model_loaded"] = self.model_loaded
        if self.model_loaded:
            result["forcefield_name"] = str(self.forcefield_name)
            result["molecule_name"] = str(self.molecule_name)
            result["molecule_format"] = self.molecule_format.value
            result["forcefield_content"] = self.forcefield_content
            result["molecule_content"] = self.molecule_content
        return result

    def from_dict(self, d: dict, version: int):
        """
        Sets the typed molecule from the dictionary representation

        Args:
            d (dict): Dictionary representation of the typed molecule
            version (int): The version of the dictionary representation

        Returns:
            None
        
        Raises:
            ValueError: If the class_name in the dictionary is not the same as the class
        """
        # Make sure that we are reading the right class
        molecule_type = d["class_name"]
        if molecule_type != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {molecule_type}.")
        super().from_dict(d, version=version)
        self.electrostatic_method = ElectrostaticMethod(
            d["electrostatic_method"])
        self.model_loaded = d.get("is_model_loaded", False)
        if not self.model_loaded:
            return
        self.forcefield_name = Path(d["forcefield_name"])
        self.molecule_name = Path(d["molecule_name"])
        self.molecule_format = MoleculeFileFormat(d["molecule_format"])
        self.forcefield_content = d["forcefield_content"]
        self.molecule_content = d["molecule_content"]
        self.load_from_string(
            self.molecule_content,
            self.molecule_format,
            self.forcefield_content,
            self.forcefield_name,
            str(self.molecule_name)
        )

    def generate_lammps_data_file(self, job_folder: Path) -> GlobalInformation:
        """
        Generates the lammps data file into a job folder. This file contains
        only the atom description and attributes (mass, position, charges) in 
        Lammps atom "full" style.

        The original molecule file as well as the forcefield file are written 
        as well in the job folder in addition to the Lammps data file.

        Args:
            job_folder (Path): The job folder

        Returns:
            GlobalInformation: The global information
        """
        # TODO: Adjust code to handle the different bbox styles
        global_info = molecule_to_lammps_data_pbc(
            self.molecule_content,
            self.molecule_format,
            job_folder,
            self.get_lammps_data_filename())

        # Copy the forcefield to the job folder
        forcefield_path = job_folder / self.forcefield_name
        with open(forcefield_path, 'w', encoding="utf-8") as f:
            f.write(self.forcefield_content)

        return global_info

    def generate_lammps_input_file(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        """
        Generates the lammps input file into a job folder. The section
        write the start of the lammps input file containing in particular 
        the unit set, the atom style declaration, the forcefield declaration, 
        and loading the data file.

        Args:
            job_folder (Path): The job folder
            global_information (GlobalInformation): The global information

        Returns:
            Path: The path to the generated lammps input file
        """
        return molecule_to_lammps_input(
            "lammps.input",
            job_folder /
            self.get_lammps_data_filename(),
            job_folder,
            Forcefield.REAX,
            self.forcefield_name,
            global_information,
            electrostatic_method=self.electrostatic_method)

    def get_lammps_data_filename(self) -> str:
        """
        Returns the name of the lammps data file as written in the lammps input file.

        Returns:
            str: The name of the lammps data file
        """
        return "model.data"

    def get_default_thermo_variables(self) -> List[str]:
        """
        Returns the default thermo variables. These variables are defined in the lammps input file 
        produced by this class and are computed from the reaxff pair style. 

        Lammps documentation: https://docs.lammps.org/pair_reaxff.html

        Returns:
            List[str]: The default thermo variables
        """
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


class AireboTypedMolecularSystem(TypedMolecularSystem):
    """
    Handler for a molecular system with a Rebo-family forcefield assigned to it. 
    This class supports rebo, airebo, and airebo-m pair styles with the type of format 
    being determined by the extension of the potential file.
    This class is responsible for generating a LAMMPS data file for the 
    system as well as the corresponding start of the input file.

    Note:
    - Only qeq and acks2 are currently supported for as electrostatic method. 
    If another method is needed, please submit a ticket on Github.

    Lammps documentation: 
        - https://docs.lammps.org/pair_airebo.html
    """

    def __init__(
            self,
            bbox_style: BoundingBoxStyle = BoundingBoxStyle.PERIODIC,
            electrostatic_method: ElectrostaticMethod = ElectrostaticMethod.QEQ):
        """
        Constructor
        Args:
            bbox_style (BoundingBoxStyle, optional): The bounding box style. Defaults to BoundingBoxStyle.PERIODIC.
            electrostatic_method (ElectrostaticMethod, optional): The electrostatic method. Defaults to ElectrostaticMethod.QEQ.
        """
        super().__init__(None, bbox_style)
        self.electrostatic_method = electrostatic_method

        self.model_loaded = False
        self.molecule_content = ""
        self.forcefield_content = ""
        self.forcefield_name = None
        self.molecule_name = None
        self.molecule_format = None
        self.atoms = None

    def get_unit_system(self) -> LammpsUnitSystem:
        """
        Returns the unit system of the system. For airebo, this is always metal.

        Returns:
            LammpsUnitSystem: The unit system of the system
        """
        return LammpsUnitSystem.METAL

    def load_from_file(
            self,
            molecule_path: Path,
            forcefield_path: Path,
            format_hint: MoleculeFileFormat = None):
        """
        Loads the molecule from a file. 

        Args:
            molecule_path (Path): The path to the molecule file
            forcefield_path (Path): The path to the forcefield file
            format_hint (MoleculeFileFormat, optional): The molecule format hint. Defaults to None.

        Raises:
            FileNotFoundError: If the molecule or forcefield file is not found
            ValueError: If the forcefield file is not a rebo forcefield
            NotImplementedError: If the molecule format is not supported
        """
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
        if forcefield_format not in [Forcefield.AIREBO, Forcefield.AIREBOM, Forcefield.REBO]:
            raise ValueError(
                f"Forcefield file {forcefield_path} is not a rebo forcefield, \
                expecting .airebo, .airebo-m, or .rebo extension, got {forcefield_path.suffix}")
        self.ff_type = forcefield_format

        # Set paths
        self.molecule_name = Path(molecule_path.name)
        self.forcefield_name = Path(forcefield_path.name)

        # Read molecule
        with open(molecule_path, "r", encoding="utf-8") as f:
            self.molecule_content = f.read()
            if format_hint is not None:
                self.molecule_format = format_hint
            elif self.molecule_name.suffix.lower() == ".xyz":
                self.molecule_format = MoleculeFileFormat.XYZ
            elif self.molecule_name.suffix.lower() == ".mol2":
                self.molecule_format = MoleculeFileFormat.MOL2
            elif self.molecule_name.suffix.lower() == ".lammpstrj":
                self.molecule_format = MoleculeFileFormat.LAMMPS_DUMP_TEXT
            else:  # Should never happen with after the format check above
                raise NotImplementedError(
                    f"Molecule format {self.molecule_name.suffix} not supported.")

        # Read forcefield
        with open(forcefield_path, "r", encoding="utf-8") as f:
            self.forcefield_content = f.read()

        # Load the ASE Atom object
        if self.molecule_format == MoleculeFileFormat.LAMMPS_DUMP_TEXT:
            with open(molecule_path, "r", encoding="utf-8") as f:
                self.atoms = ase_read_lammps_dump_text(f)
        else:
            self.atoms = ase_read(molecule_path)

        self.model_loaded = True

    def load_from_string(
            self,
            molecule_content: str,
            molecule_format: MoleculeFileFormat,
            forcefield_content: str,
            forcefield_file_name: Path,
            molecule_file_name: Path):
        """
        Loads the molecule from a string.

        Args:
            molecule_content (str): The molecule content
            molecule_format (MoleculeFileFormat): The molecule format
            forcefield_content (str): The forcefield content
            forcefield_file_name (Path): The path to the forcefield file
            molecule_file_name (Path): The path to the molecule file

        Raises:
            ValueError: If the forcefield file name does not have .airebo, .airebo-m, or .rebo extension
        """
        if forcefield_file_name.suffix.lower() not in [".airebo", ".airebo-m", ".rebo"]:
            raise ValueError(
                f"Forcefield file {forcefield_file_name} is not a rebo forcefield, \
                expecting .airebo, .airebo-m, or .rebo extension, got {forcefield_file_name.suffix.lower()}.")
        self.ff_type = get_forcefield_from_extension(forcefield_file_name.suffix)

        self.molecule_content = molecule_content
        self.molecule_format = molecule_format
        if molecule_file_name != "":
            self.molecule_name = Path(molecule_file_name)
        else:
            self.molecule_name = Path(
                "model." + get_extension_from_molecule_file_format(molecule_format))

        self.forcefield_content = forcefield_content
        self.forcefield_name = Path(forcefield_file_name)

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
        """
        Returns whether the model is loaded or not.

        Returns:
            bool: True if the model is loaded, False otherwise
        """
        return self.model_loaded

    def get_ase_model(self) -> Atoms:
        """
        Returns the ASE atoms object. If the model is not loaded, return None

        Returns:
            Atoms: The ASE atoms object
        """
        return self.atoms

    def get_molecule_content(self) -> str:
        """
        Returns the molecule content

        Returns:
            str: The molecule content
        """
        return self.molecule_content

    def get_molecule_format(self) -> MoleculeFileFormat:
        """
        Returns the molecule format

        Returns:
            MoleculeFileFormat: The molecule format
        """
        return self.molecule_format

    def get_molecule_name(self) -> Path:
        """
        Returns the molecule file name

        Returns:
            Path: The molecule file name
        """
        return self.molecule_name

    def get_forcefield_content(self) -> str:
        """
        Returns the forcefield content

        Returns:
            str: The forcefield content
        """
        return self.forcefield_content

    def get_forcefield_name(self) -> Path:
        """
        Returns the forcefield file name

        Returns:
            Path: The forcefield file name
        """
        return self.forcefield_name

    def get_electrostatic_method(self) -> ElectrostaticMethod:
        """
        Returns the electrostatic method

        Returns:
            ElectrostaticMethod: The electrostatic method
        """
        return self.electrostatic_method

    def set_electrostatic_method(self, electrostatic_method: ElectrostaticMethod):
        """
        Sets the electrostatic method

        Args:
            electrostatic_method (ElectrostaticMethod): The electrostatic method
        """
        self.electrostatic_method = electrostatic_method

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the typed molecule

        Returns:
            dict: The dictionary representation of the typed molecule
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["electrostatic_method"] = self.electrostatic_method.value
        result["is_model_loaded"] = self.model_loaded
        if self.model_loaded:
            result["forcefield_name"] = str(self.forcefield_name)
            result["molecule_name"] = str(self.molecule_name)
            result["molecule_format"] = self.molecule_format.value
            result["forcefield_content"] = self.forcefield_content
            result["molecule_content"] = self.molecule_content
        return result

    def from_dict(self, d: dict, version: int):
        """
        Sets the attributes of the typed molecule from the dictionary representation

        Args:
            d (dict): The dictionary representation of the typed molecule
            version (int): The version of the dictionary representation
        """
        # Make sure that we are reading the right class
        molecule_type = d["class_name"]
        if molecule_type != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {molecule_type}.")
        super().from_dict(d, version=version)
        self.electrostatic_method = ElectrostaticMethod(
            d["electrostatic_method"])
        self.model_loaded = d.get("is_model_loaded", False)
        if not self.model_loaded:
            return
        self.forcefield_name = Path(d["forcefield_name"])
        self.molecule_name = Path(d["molecule_name"])
        self.molecule_format = MoleculeFileFormat(d["molecule_format"])
        self.forcefield_content = d["forcefield_content"]
        self.molecule_content = d["molecule_content"]
        self.load_from_string(
            self.molecule_content,
            self.molecule_format,
            self.forcefield_content,
            self.forcefield_name,
            str(self.molecule_name)
        )

    def generate_lammps_data_file(self, job_folder: Path) -> GlobalInformation:
        """
        Generates the lammps data file into a job folder. This file contains
        only the atom description and attributes (mass, position, charges) in 
        Lammps atom "full" style.

        The original molecule file as well as the forcefield file are written 
        as well in the job folder in addition to the Lammps data file.

        Args:
            job_folder (Path): The job folder

        Returns:
            GlobalInformation: The global information
        """
        # TODO: Adjust code to handle the different bbox styles
        global_info = molecule_to_lammps_data_pbc(
            self.molecule_content,
            self.molecule_format,
            job_folder,
            self.get_lammps_data_filename())

        # Copy the forcefield to the job folder
        forcefield_path = job_folder / self.forcefield_name
        with open(forcefield_path, 'w', encoding="utf-8") as f:
            f.write(self.forcefield_content)

        return global_info

    def generate_lammps_input_file(
            self,
            job_folder: Path,
            global_information: GlobalInformation) -> Path:
        """
        Generates the lammps input file into a job folder. The section
        write the start of the lammps input file containing in particular 
        the unit set, the atom style declaration, the forcefield declaration, 
        and loading the data file.

        Args:
            job_folder (Path): The job folder
            global_information (GlobalInformation): The global information

        Returns:
            Path: The path to the generated lammps input file
        """
        return molecule_to_lammps_input(
            "lammps.input",
            job_folder /
            self.get_lammps_data_filename(),
            job_folder,
            self.ff_type,
            self.forcefield_name,
            global_information,
            electrostatic_method=self.electrostatic_method)

    def get_lammps_data_filename(self) -> str:
        """
        Returns the name of the lammps data file as written in the lammps input file.

        Returns:
            str: The name of the lammps data file
        """
        return "model.data"

    def get_default_thermo_variables(self) -> List[str]:
        """
        Returns the default thermo variables. These variables are defined in the lammps input file 
        produced by this class and are computed from the airebo pair style. 

        Lammps documentation: https://docs.lammps.org/pair_airebo.html

        Returns:
            List[str]: The default thermo variables
        """
        return [
            'step',
            'v_REBO',
            'v_LJ',
            'v_TORSION']
