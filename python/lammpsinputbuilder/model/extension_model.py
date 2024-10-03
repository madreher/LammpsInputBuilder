from typing import Union, Annotated, Literal

from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.quantity_model import TemperatureQuantityModel, ForceQuantityModel, \
    VelocityQuantityModel
from lammpsinputbuilder.model.instruction_model import InstructionModel

class ExtensionModel(BaseObjectModel):
    pass

class LangevinExtensionModel(ExtensionModel):
    class_name: Literal["LangevinExtension"]
    group_name: str
    start_temp: TemperatureQuantityModel
    end_temp: TemperatureQuantityModel
    damp: TemperatureQuantityModel
    seed: int

class SetForceExtensionModel(ExtensionModel):
    class_name: Literal["SetForceExtension"]
    group_name: str
    fx: ForceQuantityModel
    fy: ForceQuantityModel
    fz: ForceQuantityModel

class MoveExtensionModel(ExtensionModel):
    class_name: Literal["MoveExtension"]
    group_name: str
    vx: VelocityQuantityModel
    vy: VelocityQuantityModel
    vz: VelocityQuantityModel

class InstructionExtensionModel(ExtensionModel):
    class_name: Literal["InstructionExtension"]
    instruction: InstructionModel

class ManualExtensionModel(ExtensionModel):
    class_name: Literal["ManualExtension"]
    do_cmd: str
    undo_cmd: str

ExtensionUnion = Annotated[Union[
    LangevinExtensionModel,
    SetForceExtensionModel,
    MoveExtensionModel,
    InstructionExtensionModel,
    ManualExtensionModel],
    Field(discriminator="class_name")]
