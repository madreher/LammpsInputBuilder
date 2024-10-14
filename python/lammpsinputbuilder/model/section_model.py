from typing import List, Literal
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.group_model import GroupUnion
from lammpsinputbuilder.model.instruction_model import InstructionUnion
from lammpsinputbuilder.model.extension_model import ExtensionUnion
from lammpsinputbuilder.model.fileio_model import FileIOUnion
from lammpsinputbuilder.model.integrator_model import IntegratorUnion

class SectionModel(BaseObjectModel):
    pass

class IntegratorSectionModel(SectionModel):
    class_name: Literal["IntegratorSection"]
    groups: List[GroupUnion] = Field(
        default=[],
        description=("List of groups to include in the section.")
    )
    instructions: List[InstructionUnion] = Field(
        default=[],
        description=("List of instructions to include in the section.")
    )
    fileios: List[FileIOUnion] = Field(
        default=[],
        description=("List of fileio to include in the section.")
    )
    extensions: List[ExtensionUnion] = Field(
        default=[],
        description=("List of extensions to include in the section.")
    )
    post_extensions: List[ExtensionUnion] = Field(
        default=[],
        description=("List of post-extensions to include in the section.")
    )
    integrator: IntegratorUnion = Field(
        description=("The integrator to include in the section.")
    )

    class Config:
        title = "IntegratorSection"
        json_schema_extra = {
            "description": ("Section to execute an integrator with its associated "
                            "groups, instructions, fileio, extensions and post-extensions.")
        }

class InstructionsSectionModel(SectionModel):
    class_name: Literal["InstructionsSection"]
    instructions: List[InstructionUnion] = Field(
        default=[],
        description=("List of instructions to include in the section.")
    )

    class Config:
        title = "InstructionsSection"
        json_schema_extra = {
            "description": ("Section to execute instructions only. "
                            "Typically used between other sections.")
        }
