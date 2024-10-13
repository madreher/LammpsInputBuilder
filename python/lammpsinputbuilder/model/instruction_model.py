from typing import Union, Annotated, Literal, Optional
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.quantity_model import TimeQuantityModel, TemperatureQuantityModel, \
    LengthQuantityModel
from lammpsinputbuilder.instructions import VariableStyle


class InstructionModel(BaseObjectModel):
    pass

class ResetTimestepInstructionModel(InstructionModel):
    class_name: Literal["ResetTimestepInstruction"]
    new_timestep: int = Field(
        description=("New counter for the timestep. Default is 0. "
                     "Lammps documentation: https://docs.lammps.org/reset_timestep.html"),
        default=0
    )

    class Config:
        title = "ResetTimestepInstruction"
        json_schema_extra = {
            "description": ("Resets the timestep counter. "
                            "Lammps documentation: https://docs.lammps.org/reset_timestep.html")
        }

class SetTimestepInstructionModel(InstructionModel):
    class_name: Literal["SetTimestepInstruction"]
    timestep: TimeQuantityModel = Field(
        description=("New integration timestep in time units. "
                     "Lammps documentation: https://docs.lammps.org/timestep.html")
    )

    class Config:
        title = "SetTimestepInstruction"
        json_schema_extra = {
            "description": ("Sets the integration timestep. "
                            "Lammps documentation: https://docs.lammps.org/timestep.html")
        }

class VelocityCreateInstructionModel(InstructionModel):
    class_name: Literal["VelocityCreateInstruction"]
    group_name: str = Field(
        description=("Name of a group to set the atom forces to. "
                     "The given group must exist. "
                     "If not set, the forces are applied to the \"all\" group. "
                     "Lammps documentation: https://docs.lammps.org/velocity.html"),
        default="all"
    )
    temp: TemperatureQuantityModel = Field(
        description=("The temperature used to generate the corresponing velocity vectors. ")
    )
    seed: int = Field(
        description=("Seed for the random number generator.")
    )

    class Config:
        title = "VelocityCreateInstruction"
        json_schema_extra = {
            "description": ("Sets the velocity of a group of atoms. "
                            "Lammps documentation: https://docs.lammps.org/velocity.html")
        }

class VariableInstructionModel(InstructionModel):
    class_name: Literal["VariableInstruction"]
    variable_name: str = Field(
        description=("Name of the variable to set. "
                     "Lammps documentation: https://docs.lammps.org/variable.html"),
    )
    style: VariableStyle = Field(
        description=("Style of the variable, i.e how to define the variable value. ")
    )
    args: str = Field(
        description=("Arguments for the variable to apply after the style. Given each style "
                     "expects different arguments, there is no validation done on the args. ")
    )

    class Config:
        title = "VariableInstruction"
        json_schema_extra = {
            "description": ("Assigns one or more strings to a variable name for evaluation "
                            "later in the input script or during a simulation. "
                            "Lammps documentation: https://docs.lammps.org/variable.html")
        }

class DisplaceAtomsInstructionModel(InstructionModel):
    class_name: Literal["DisplaceAtomsInstruction"]
    group_name: str = Field(
        description=("Name of a group to apply the translation to.")
    )
    dx: Optional[LengthQuantityModel] = Field(
        description=("Displacement in x direction. ")
    )
    dy: Optional[LengthQuantityModel] = Field(
        description=("Displacement in y direction. ")
    )
    dz: Optional[LengthQuantityModel] = Field(
        description=("Displacement in z direction. ")
    )

    class Config:
        title = "DisplaceAtomsInstruction"
        json_schema_extra = {
            "description": ("Displaces atoms in a group. "
                            "Lammps documentation: https://docs.lammps.org/displace_atoms.html")
        }

class ManualInstructionModel(InstructionModel):
    class_name: Literal["ManualInstruction"]
    cmd: str = Field(
        description=("Command(s) to execute. ")
    )

    class Config:
        title = "ManualInstruction"
        json_schema_extra = {
            "description": ("Execute arbitrary command(s) provided by the user. "
                            "Multiple commands can be provided separated by newlines. ")
        }

InstructionUnion = Annotated[Union[
    ResetTimestepInstructionModel,
    SetTimestepInstructionModel,
    VelocityCreateInstructionModel,
    VariableInstructionModel,
    DisplaceAtomsInstructionModel,
    ManualInstructionModel
    ], Field(discriminator="class_name")]
