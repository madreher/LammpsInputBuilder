"""Module for the integrator class."""

from enum import IntEnum

from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.base import BaseObject


class Integrator(BaseObject):
    """
    Base class for Lammps methods to perform a timestepping process.
    This includes any operation which may affect the step counter of the simulation.
    In most cases, the integrator represents a time integration method but it also 
    includes geometry optimization methods or simple "run" commands without a particular 
    method attached to it.

    An integrator has a scope, and therfor must provide a way to declare the 
    computations, but also how to un-declare them. This is done by overriding
    the `add_do_commands()`, `add_undo_commands()`, and `add_run_commands()` methods. 
    Each subclass implementing a new Integrator must implement these methods.

    This class should never be instantiated directly. Instead, the subclasses
    should implement the `add_do_commands()`, `add_undo_commands()`, and `add_run_commands()` methods.
    """

    def __init__(self, integrator_name: str = "defaultIntegrator") -> None:
        """
        Constructor
        Args:
            integrator_name (str, optional): The name of the integrator. Defaults to "defaultIntegrator".

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(id_name=integrator_name)

    def get_integrator_name(self) -> str:
        """
        Get the name of the integrator
        Returns:
            str: The name of the integrator
        """
        return super().get_id_name()

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the integrator.
        Returns:
            dict: The dictionary representation of the integrator.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Generate the commands to perform the computations
        Args:
            global_information (GlobalInformation): The global information for the workflow
        Returns:
            str: The commands to perform the computations
        """
        del global_information  # unused
        return ""

    def add_undo_commands(self) -> str:
        """
        Generate the commands to undo the computations
        Returns:
            str: The commands to undo the computations
        """
        return ""

    def add_run_commands(self) -> str:
        """
        Generate the commands to advance the step counter
        Returns:
            str: The commands to advance the step counter
        """
        return ""


class RunZeroIntegrator(Integrator):
    """
    Class for the RunZero integrator. The RunZero integrator is used to 
    compute a single point energy calculation. With this integrator, various 
    system quantities are computed but the molecule system is not changed as a result.
    This integrator can be used to trigger file outputs, obtain thermo outputs, etc.
    The step counter is not advanced as a result of this integrator.
    """
    def __init__(self, integrator_name: str = "RunZero") -> None:
        """
        Constructor
        Args:
            integrator_name (str, optional): The name of the integrator. Defaults to "RunZero".

        Returns:
            None
        """
        super().__init__(integrator_name=integrator_name)

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the integrator.
        Returns:
            dict: The dictionary representation of the integrator.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.
        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None
        
        Raise:
            ValueError: If the class name in the dictionary is not the same as the current class
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)

    def add_run_commands(self) -> str:
        """
        Generate the commands to advance the step counter
        Returns:
            str: The commands to advance the step counter
        """
        return "run 0\n"


class NVEIntegrator(Integrator):
    """
    Class for the NVE integrator. The NVE integrator is used to perform
    a plain time integration to update position and velocity for atoms in 
    the group each timestep. This creates a system trajectory consistent 
    with the microcanonical ensemble (NVE) provided there are (full) periodic boundary 
    conditions and no other “manipulations” of the system (e.g. fixes that modify
    forces or velocities).

    Lammps documentation: https://docs.lammps.org/fix_nve.html
    """
    def __init__(
            self,
            integrator_name: str = "NVEID",
            group: Group = AllGroup(),
            nb_steps: int = 5000) -> None:
        """
        Constructor
        Args:
            integrator_name (str, optional): The name of the integrator. Defaults to "NVEID".
            group (Group, optional): The group to apply the integrator to. Defaults to AllGroup().
            nb_steps (int, optional): The number of steps to perform. Defaults to 5000.

        Returns:
            None

        Raise:
            ValueError: If the integrator_name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(integrator_name=integrator_name)
        self.group = group.get_group_name()
        self.nb_steps = nb_steps

    def get_group_name(self) -> str:
        """
        Get the name of the group to apply the integrator to
        Returns:
            str: The name of the group to apply the integrator to
        """
        return self.group

    def get_nb_steps(self) -> int:
        """
        Get the number of steps to perform
        Returns:
            int: The number of steps to perform
        """
        return self.nb_steps

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the integrator.
        Returns:
            dict: The dictionary representation of the integrator.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["group_name"] = self.group
        result["nb_steps"] = self.nb_steps
        return result

    def from_dict(self, d: dict, version: int):
        """
        Parse the dictionary representation of the workflow and load it into 
        the current object.
        Args:
            d (dict): The dictionary representation of the workflow.
            version (int): The version of the dictionary representation.

        Returns:
            None
        
        Raise:
            ValueError: If the class name in the dictionary is not the same as the current class
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.group = d["group_name"]
        self.nb_steps = d.get("nb_steps", 5000)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Generate the commands to apply the integrator
        Args:
            global_information (GlobalInformation): Data handler containing information
                                                    related to the entire workflow

        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        return f"fix {self.get_integrator_name()} {self.group} nve\n"

    def add_undo_commands(self) -> str:
        """
        Generate the commands to undo the integrator
        Returns:
            str: Lammps command(s)
        """
        return f"unfix {self.get_integrator_name()}\n"

    def add_run_commands(self) -> str:
        """
        Generate the commands to advance the step counter
        Returns:
            str: The commands to advance the step counter
        """
        return f"run {self.nb_steps}\n"


class MinimizeStyle(IntEnum):
    CG = 0
    SD = 1
    SPIN_LBFGS = 2


class MinimizeIntegrator(Integrator):
    """
    Class for the Minimize integrator. The Minimize integrator is used to perform
    a geometry optimization on a molecular system by iteratively adjusting atom coordinates. 
    Iterations are terminated when one of the stopping criteria is satisfied. At that point
    the configuration will hopefully be in a local potential energy minimum.

    The MinimizeIntegrator currently only support the cg, sd, and spin/lbfgs methods. For 
    other style of minimizations, please use the ManualIntegrator.

    IMPORTANT: The MinimizerIntegrator always apply to the entire molecular system.

    Lammps documentation: https://docs.lammps.org/minimize.html
    """

    minimizeStyleToStr = {
        MinimizeStyle.CG: "cg",
        MinimizeStyle.SD: "sd",
        MinimizeStyle.SPIN_LBFGS: "spin/lbfgs"
    }

    def __init__(
            self,
            integrator_name: str = "Minimize",
            style: MinimizeStyle = MinimizeStyle.CG,
            etol: float = 0.01,
            ftol: float = 0.01,
            maxiter: int = 100,
            maxeval: int = 10000) -> None:
        """
        Constructor
        Args:
            integrator_name (str, optional): The name of the integrator. Defaults to "Minimize".
            style (MinimizeStyle, optional): The style of the minimization. Defaults to MinimizeStyle.CG.
            etol (float, optional): The energy tolerance. Defaults to 0.01.
            ftol (float, optional): The force tolerance. Defaults to 0.01.
            maxiter (int, optional): The maximum number of iterations. Defaults to 100.
            maxeval (int, optional): The maximum number of function evaluations. Defaults to 10000.

        Returns:
            None

        Raise:
            ValueError: If the integrator_name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(integrator_name=integrator_name)
        self.style = style
        self.etol = etol
        self.ftol = ftol
        self.maxiter = maxiter
        self.maxeval = maxeval

    def get_minimize_style(self) -> MinimizeStyle:
        """
        Get the style of the minimization
        Returns:
            MinimizeStyle: The style of the minimization
        """
        return self.style

    def get_etol(self) -> float:
        """
        Get the energy tolerance
        Returns:
            float: The energy tolerance
        """
        return self.etol

    def get_ftol(self) -> float:
        """
        Get the force tolerance
        Returns:
            float: The force tolerance
        """
        return self.ftol

    def get_maxiter(self) -> int:
        """
        Get the maximum number of iterations
        Returns:
            int: The maximum number of iterations
        """
        return self.maxiter

    def get_maxeval(self) -> int:
        """
        Get the maximum number of function evaluations
        Returns:
            int: The maximum number of function evaluations
        """
        return self.maxeval

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the MinimizeIntegrator
        Returns:
            dict: The dictionary representation of the MinimizeIntegrator
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["style"] = self.style.value
        result["etol"] = self.etol
        result["ftol"] = self.ftol
        result["maxiter"] = self.maxiter
        result["maxeval"] = self.maxeval
        return result

    def from_dict(self, d: dict, version: int):
        """
        Initializes the MinimizeIntegrator from a dictionary
        Args:
            d (dict): The dictionary representation of the MinimizeIntegrator
            version (int): The version of the dictionary format

        Returns:
            None
        """
        if version != 0:
            raise ValueError(f"Unsupported version {version}.")
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.style = MinimizeStyle(d["style"])
        self.etol = d["etol"]
        self.ftol = d["ftol"]
        self.maxiter = d["maxiter"]
        self.maxeval = d["maxeval"]

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Adds the do commands for the MinimizeIntegrator
        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        return ""

    def add_undo_commands(self) -> str:
        """
        Adds the undo commands for the MinimizeIntegrator
        Returns:
            str: Lammps command(s)
        """
        return ""

    def add_run_commands(self) -> str:
        """
        Adds the run commands for the MinimizeIntegrator
        Returns:
            str: Lammps command(s)
        """
        result = f"min_style {MinimizeIntegrator.minimizeStyleToStr[self.style]}\n"
        result += f"minimize {self.etol} {self.ftol} {self.maxiter} {self.maxeval}\n"
        return result


class MultipassMinimizeIntegrator(Integrator):
    """
    Class implementing a multi-pass minimization process. For each pass, the integrator 
    will perform multiple minimization with a different style for each minimization. 
    Between two passes, the integrator check if the energy difference between the last two 
    minimization passes have changed. If the energy difference is smaller than a threshold, then
    the process stops.
    """
    def __init__(self, integrator_name: str = "MultiMinimize") -> None:
        """
        Initializes a new instance of the MultipassMinimizeIntegrator class.
        Args:
            integrator_name (str): The name of the integrator. Defaults to "MultiMinimize".
        Returns:
            None
        Raise:
            ValueError: If the integrator_name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(integrator_name=integrator_name)

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the MultipassMinimizeIntegrator
        Returns:
            dict: The dictionary representation of the MultipassMinimizeIntegrator
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        """
        Initializes the MultipassMinimizeIntegrator from a dictionary
        Args:
            d (dict): The dictionary representation of the MultipassMinimizeIntegrator
            version (int): The version of the dictionary format

        Returns:
            None
        
        Raise:
            ValueError: If the class name is not found or the same as the current class
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Adds the do commands for the MultipassMinimizeIntegrator
        Args:
            global_information (GlobalInformation): The global information

        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        return ""

    def add_undo_commands(self) -> str:
        """
        Adds the undo commands for the MultipassMinimizeIntegrator
        Returns:
            str: Lammps command(s)
        """
        return ""

    def add_run_commands(self) -> str:
        """
        Adds the run commands for the MultipassMinimizeIntegrator
        Returns:
            str: Lammps command(s)
        """
        commands = ""
        commands += "min_style      cg\n"
        commands += "minimize       1.0e-10 1.0e-10 10000 100000\n"

        commands += "min_style      hftn\n"
        commands += "minimize       1.0e-10 1.0e-10 10000 100000\n"

        commands += 'min_style      sd\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'variable       i loop 100\n'
        commands += 'label          loop1\n'
        commands += 'variable       ene_min equal pe\n'
        commands += 'variable       ene_min_i equal ${ene_min}\n'

        commands += 'min_style      cg\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'min_style      hftn\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'min_style      sd\n'
        commands += 'minimize       1.0e-10 1.0e-10 10000 100000\n'

        commands += 'variable       ene_min_f equal pe\n'
        commands += 'variable       ene_diff equal ${ene_min_i}-${ene_min_f}\n'
        commands += 'print          "Delta_E = ${ene_diff}"\n'
        commands += 'if             "${ene_diff}<1e-6" then "jump SELF break1"\n'
        commands += 'print          "Loop_id = $i"\n'
        commands += 'next           i\n'
        commands += 'jump           SELF loop1\n'
        commands += 'label          break1\n'
        commands += 'variable       i delete\n'
        return commands


class ManualIntegrator(Integrator):
    """
    Class for the Manual integrator. The Manual integrator is used to implement 
    a integrator which cannot be derived from the other available integrators.
    The ManuelIntegrator offers a way for users to define their own integrators by 
    providing the do, undo, and run commands. 

    If an Integrator is missing from the library, please submit an issue to the Github repository.
    """
    def __init__(
            self,
            integrator_name: str = "Manual",
            cmd_do: str = "",
            cmd_undo: str = "",
            cmd_run: str = "") -> None:
        """
        Constructor
        Args:
            integrator_name (str): The name of the integrator. Defaults to "Manual".
            cmd_do (str): The do command. Defaults to "".
            cmd_undo (str): The undo command. Defaults to "".
            cmd_run (str): The run command. Defaults to "".

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(integrator_name=integrator_name)
        self.cmd_do = cmd_do
        self.cmd_undo = cmd_undo
        self.cmd_run = cmd_run

    def get_do_commands(self) -> str:
        """
        Returns the do commands
        Returns:
            str: Lammps command(s)
        """
        return self.cmd_do

    def get_undo_commands(self) -> str:
        """
        Returns the undo commands
        Returns:
            str: Lammps command(s)
        """
        return self.cmd_undo

    def get_run_commands(self) -> str:
        """
        Returns the run commands
        Returns:
            str: Lammps command(s)
        """
        return self.cmd_run

    def to_dict(self) -> dict:
        """
        Returns the integrator as a dictionary
        Returns:
            dict: The dictionary representation of the integrator
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["cmd_do"] = self.cmd_do
        result["cmd_undo"] = self.cmd_undo
        result["cmd_run"] = self.cmd_run
        return result

    def from_dict(self, d: dict, version: int):
        """
        Loads the integrator from a dictionary
        Args:
            d (dict): The dictionary representation of the integrator
            version (int): The version of the dictionary representation
        Returns:
            None
        Raise:
            ValueError: If the class name in the dictionary is not the same as the current class
        """
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version)
        self.cmd_do = d["cmd_do"]
        self.cmd_undo = d["cmd_undo"]
        self.cmd_run = d["cmd_run"]

    def add_do_commands(self, global_information: GlobalInformation) -> str:
        """
        Adds the do commands
        Args:
            global_information (GlobalInformation): The global information
        Returns:
            str: Lammps command(s)
        """
        del global_information  # unused
        if self.cmd_do.endswith("\n"):
            return self.cmd_do
        return self.cmd_do + "\n"

    def add_undo_commands(self) -> str:
        """
        Adds the undo commands
        Returns:
            str: Lammps command(s)
        """
        if self.cmd_undo.endswith("\n"):
            return self.cmd_undo
        return self.cmd_undo + "\n"

    def add_run_commands(self) -> str:
        """
        Adds the run commands
        Returns:
            str: Lammps command(s)
        """
        if self.cmd_run.endswith("\n"):
            return self.cmd_run
        return self.cmd_run + "\n"
