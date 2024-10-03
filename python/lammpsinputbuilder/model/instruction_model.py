from typing import Union, Annotated, Literal
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.quantity_model import TimeQuantityModel, TemperatureQuantityModel, \
    LengthQuantityModel


class InstructionModel(BaseObjectModel):
    pass

class ResetTimestepInstructionModel(InstructionModel):
    class_name: Literal["ResetTimestepInstruction"]
    new_timestep: int

class SetTimestepInstructionModel(InstructionModel):
    class_name: Literal["SetTimestepInstruction"]
    timestep: TimeQuantityModel

class VelocityCreateInstructionModel(InstructionModel):
    class_name: Literal["VelocityCreateInstruction"]
    group_name: str
    temp: TemperatureQuantityModel
    seed: int

class VariableInstructionModel(InstructionModel):
    class_name: Literal["VariableInstruction"]
    variable_name: str
    style: int
    args: str

class DisplaceAtomsInstructionModel(InstructionModel):
    class_name: Literal["DisplaceAtomsInstruction"]
    group_name: str
    dx: LengthQuantityModel
    dy: LengthQuantityModel
    dz: LengthQuantityModel

class ManualInstructionModel(InstructionModel):
    class_name: Literal["ManualInstruction"]
    cmd: str

InstructionUnion = Annotated[Union[
    ResetTimestepInstructionModel,
    SetTimestepInstructionModel,
    VelocityCreateInstructionModel,
    VariableInstructionModel,
    DisplaceAtomsInstructionModel,
    ManualInstructionModel
    ], Field(discriminator="class_name")]
