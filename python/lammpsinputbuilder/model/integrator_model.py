from typing import Union, Annotated, Literal
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.integrator import MinimizeStyle

class IntegratorModel(BaseObjectModel):
    pass

class RunZeroIntegratorModel(IntegratorModel):
    class_name: Literal["RunZeroIntegrator"]

    class Config:
        title = "RunZeroIntegrator"
        json_schema_extra = {
            "description": ("Simple integrator executing a \"run 0\" command. ")
        }

class NVEIntegratorModel(IntegratorModel):
    class_name: Literal["NVEIntegrator"]
    group_name:str = Field(
        description=("Name of a group to apply the integrator to.",
                     "The given group must exist. "
                     "If not set, the integrator is applied to the \"all\" group."),
        default="all"
    )
    nb_steps:int = Field(
        description=("The number of time steps to run.")
    )

    class Config:
        title = "NVEIntegrator"
        json_schema_extra = {
            "description": ("Run a nve for a given number of steps on a group. "
                            "Lammps documentation: https://docs.lammps.org/fix_nve.html")
        }

class MinimizeIntegratorModel(IntegratorModel):
    class_name: Literal["MinimizeIntegrator"]
    style:MinimizeStyle = Field(
        description=("Minimization algorithm to use. ")
    )
    etol:float = Field(
        description=("Stopping tolerance for energy (unitless).")
    )
    ftol:float = Field(
        description=("Stopping tolerance for force (force units).")
    )
    maxiter:int = Field(
        description=("Max iterations of minimizer.")
    )
    maxeval:int = Field(
        description=("Max number of force/energy evaluations.")
    )

    class Config:
        title = "MinimizeIntegrator"
        json_schema_extra = {
            "description": ("Perform an energy minimization of the system, by iteratively adjusting"
                            " atom coordinates. Iterations are terminated when one of the stopping "
                            "criteria is satisfied."
                            "Lammps documentation: https://docs.lammps.org/minimize.html")
        }

class MultiPassMinimizeIntegratorModel(IntegratorModel):
    class_name: Literal["MultipassMinimizeIntegrator"]

    class Config:
        title = "MultipassMinimizeIntegrator"
        json_schema_extra = {
            "description": ("Perform multiple passes of energy minimization on the system. "
                            "This is meant to be a fixed protocol to minimize systems using "
                            "a reax of rebo like potentials.")
        }

class ManualIntegratorModel(IntegratorModel):
    class_name: Literal["ManualIntegrator"]
    cmd_do:str = Field(
        description=("Command to execute te declare the time integration process.")
    )
    cmd_undo:str = Field(
        description=("Command to execute to undo the time integration process.")
    )
    cmd_run:str = Field(
        description=("Command to execute to run the time integration process.")
    )

    class Config:
        title = "ManualIntegrator"
        json_schema_extra = {
            "description": ("Execute arbitrary command(s) provided by the user to "
                            "declare, run, and remove a time integration process. "
                            "Multiple commands can be provided separated by newlines. ")
        }

IntegratorUnion = Annotated[Union [
    RunZeroIntegratorModel,
    NVEIntegratorModel,
    MinimizeIntegratorModel,
    MultiPassMinimizeIntegratorModel,
    ManualIntegratorModel
    ], Field(discriminator="class_name")]
