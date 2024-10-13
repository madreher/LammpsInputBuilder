from typing import Union, Annotated, Literal, Optional

from pydantic import Field, PositiveInt
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.quantity_model import TemperatureQuantityModel, ForceQuantityModel, \
    VelocityQuantityModel
from lammpsinputbuilder.model.instruction_model import InstructionUnion

class ExtensionModel(BaseObjectModel):
    pass

class LangevinExtensionModel(ExtensionModel):
    class_name: Literal["LangevinExtension"]
    group_name: str = Field(
        description=("Name of a group to apply the extension to. "
                     "The given group must exist. "
                     "If not set, the extension is applied to the \"all\" group."),
        default="all")
    start_temp: TemperatureQuantityModel = Field(
        description="Initial temperature for the thermostat."
    )
    end_temp: TemperatureQuantityModel = Field(
        description=("Temptative final temperature for the thermostat. "
        "Note that this temperature is not guaranteed to be reached.")
    )
    damp: TemperatureQuantityModel = Field(
        description=("Determines how rapidly the temperature is relaxed. For example, "
        "a value of 100.0 means to relax the temperature in a timespan of (roughly) 100 time units")
    )
    seed: PositiveInt = Field(
        description="Seed for the random number generator."
    )

    class Config:
        title = "LangevinExtension"
        json_schema_extra = {
            "description": ("Apply a Langevin thermostat on a group of atoms. "
                            "Lammps documentation: https://docs.lammps.org/fix_langevin.html")
        }

class SetForceExtensionModel(ExtensionModel):
    class_name: Literal["SetForceExtension"]
    group_name: str = Field(
        description=("Name of a group to apply the extension to. "
                     "The given group must exist. "
                     "If not set, the extension is applied to the \"all\" group."),
        default="all")
    fx: Optional[ForceQuantityModel] = Field(
        description="The force to set the atoms to for the x component."
    )
    fy: Optional[ForceQuantityModel] = Field(
        description="The force to set the atoms to for the y component."
    )
    fz: Optional[ForceQuantityModel] = Field(
        description="The force to set the atoms to for the z component."
    )

    class Config:
        title = "SetForceExtension"
        json_schema_extra = {
            "description": ("Fix the force vector of a group of atoms. "
                            "Lammps documentation: https://docs.lammps.org/fix_setforce.html")
        }

class MoveExtensionModel(ExtensionModel):
    class_name: Literal["MoveExtension"]
    group_name: str = Field(
        description=("Name of a group to apply the extension to. "
                     "The given group must exist. "
                     "If not set, the extension is applied to the \"all\" group."),
        default="all")
    vx: Optional[VelocityQuantityModel] = Field(
        description="The velocity to set the atoms to for the x component."
    )
    vy: Optional[VelocityQuantityModel] = Field(
        description="The velocity to set the atoms to for the y component."
    )
    vz: Optional[VelocityQuantityModel] = Field(
        description="The velocity to set the atoms to for the z component."
    )

    class Config:
        title = "MoveExtension"
        json_schema_extra = {
            "description": ("Apply a velocity vector to a group of atoms. "
                            "The move command is currently forced to be linear. "
                            "Use the ManualExtensionModel if another profile is needed. "
                            "Lammps documentation: https://docs.lammps.org/fix_move.html")
        }

class InstructionExtensionModel(ExtensionModel):
    class_name: Literal["InstructionExtension"]
    instruction: InstructionUnion = Field(
        description=("The instruction to process instead of an extension. "
                     "The instruction command will be written when the add_do_commands "
                     "method of the Extension is called.")
    )

    class Config:
        title = "InstructionExtension"
        json_schema_extra = {
            "description": ("Convert an Instruction object into an Extension object."
                            " The Instruction command is written when the add_do_commands "
                            "method of the Extension is called.")
        }

class ManualExtensionModel(ExtensionModel):
    class_name: Literal["ManualExtension"]
    do_cmd: str = Field(
        description=("The Lammps command(s) to execute when the add_do_commands method is called. "
                    "The field can contain multiple commands separated by newlines.")
    )
    undo_cmd: str = Field(
        description=("The Lammps command(s) to execute when the add_undo_commands method is called."
                    " The field can contain multiple commands separated by newlines.")
    )

    class Config:
        title = "ManualExtension"
        json_schema_extra = {
            "description": ("Extension fully written by the user. The user is responsible for "
                            "writing the commands in the do_cmd and undo_cmd sections. "
                            "Note that no verifications can be done on the commands and are the"
                            " sole responsibility of the user.")
        }

ExtensionUnion = Annotated[Union[
    LangevinExtensionModel,
    SetForceExtensionModel,
    MoveExtensionModel,
    InstructionExtensionModel,
    ManualExtensionModel],
    Field(discriminator="class_name")]
