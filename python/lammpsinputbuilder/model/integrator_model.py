from typing import Union, Annotated, Literal
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.integrator import MinimizeStyle

class IntegratorModel(BaseObjectModel):
    pass

class RunZeroIntegratorModel(IntegratorModel):
    class_name: Literal["RunZeroIntegrator"]

class NVEIntegratorModel(IntegratorModel):
    class_name: Literal["NVEIntegrator"]
    group_name:str
    nb_steps:int

class MinimizeIntegratorModel(IntegratorModel):
    class_name: Literal["MinimizeIntegrator"]
    style:MinimizeStyle
    etol:float
    ftol:float
    maxiter:int
    maxeval:int

class MultiPassMinimizeIntegratorModel(IntegratorModel):
    class_name: Literal["MultipassMinimizeIntegrator"]

class ManualIntegratorModel(IntegratorModel):
    class_name: Literal["ManualIntegrator"]
    cmd_do:str
    cmd_undo:str
    cmd_run:str

IntegratorUnion = Annotated[Union [
    RunZeroIntegratorModel,
    NVEIntegratorModel,
    MinimizeIntegratorModel,
    MultiPassMinimizeIntegratorModel,
    ManualIntegratorModel
    ], Field(discriminator="class_name")]
