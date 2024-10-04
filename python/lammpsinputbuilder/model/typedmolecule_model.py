from typing import Union, Literal, Annotated
from pydantic import BaseModel, Field

class TypedMolecularSystemModel(BaseModel):
    forcefield: int
    bbox_style: int

class ReaxTypedMolecularSystemModel(TypedMolecularSystemModel):
    class_name: Literal["ReaxTypedMolecularSystem"]
    electrostatic_method: int
    forcefield_name: str
    molecule_name: str
    molecule_format: int
    forcefield_content: str
    molecule_content: str

class AireboTypedMolecularSystemModel(TypedMolecularSystemModel):
    class_name: Literal["AireboTypedMolecularSystem"]
    electrostatic_method: int
    forcefield_name: str
    molecule_name: str
    molecule_format: int
    forcefield_content: str
    molecule_content: str

# Not doing a Annoted for now, it requires at least two objects
TypedMolecularSystemUnion = Annotated[Union[ReaxTypedMolecularSystemModel, AireboTypedMolecularSystemModel], Field(discriminator="class_name")]
