from typing import Union, Literal, Annotated
from pydantic import BaseModel, Field
from lammpsinputbuilder.types import Forcefield, BoundingBoxStyle, ElectrostaticMethod, MoleculeFileFormat

class TypedMolecularSystemModel(BaseModel):
    forcefield: Forcefield = Field(
        description="Type of forcefield used for the system",
    )
    bbox_style: BoundingBoxStyle = Field(
        description=("Type of bounding box used for the system. "
                     "Support periodic and shrink bounding boxes.")
    )

class ReaxTypedMolecularSystemModel(TypedMolecularSystemModel):
    class_name: Literal["ReaxTypedMolecularSystem"]
    electrostatic_method: ElectrostaticMethod = Field(
        description=("Type of electrostatic method used for the system. "
                     "Support ACKS2 and QEQ.")
    )
    forcefield_name: str = Field(
        description="Name of the file containing the forcefield parameters."
    )
    molecule_name: str = Field(
        description="Name of the file containing the atom positions of the system."
    )
    molecule_format: MoleculeFileFormat = Field(
        description="Format of the molecule file. Support xyz, mol2, and lammpstrj."
    )
    forcefield_content: str = Field(
        description="Content of the forcefield file."
    )
    molecule_content: str = Field(
        description="Content of the molecule file, i.e the atom positions in text format."
    )

class AireboTypedMolecularSystemModel(TypedMolecularSystemModel):
    class_name: Literal["AireboTypedMolecularSystem"]
    electrostatic_method: ElectrostaticMethod = Field(
        description=("Type of electrostatic method used for the system. "
                     "Support ACKS2 and QEQ.")
    )
    forcefield_name: str = Field(
        description="Name of the file containing the forcefield parameters."
    )
    molecule_name: str = Field(
        description="Name of the file containing the atom positions of the system."
    )
    molecule_format: MoleculeFileFormat = Field(
        description="Format of the molecule file. Support xyz, mol2, and lammpstrj."
    )
    forcefield_content: str = Field(
        description="Content of the forcefield file."
    )
    molecule_content: str = Field(
        description="Content of the molecule file, i.e the atom positions in text format."
    )

# Not doing a Annoted for now, it requires at least two objects
TypedMolecularSystemUnion = Annotated[
    Union[
        ReaxTypedMolecularSystemModel,
        AireboTypedMolecularSystemModel
        ],
        Field(discriminator="class_name")]
