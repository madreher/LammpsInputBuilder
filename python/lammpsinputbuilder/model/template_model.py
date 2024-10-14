from __future__ import annotations
from typing import List, Union, Literal, Annotated
from pydantic import Field
from lammpsinputbuilder.model.section_model import SectionModel, \
    IntegratorSectionModel, InstructionsSectionModel
from lammpsinputbuilder.model.fileio_model import FileIOUnion
from lammpsinputbuilder.model.group_model import GroupUnion
from lammpsinputbuilder.model.extension_model import ExtensionUnion
from lammpsinputbuilder.model.instruction_model import InstructionUnion
from lammpsinputbuilder.integrator import MinimizeStyle

class TemplateSectionModel(SectionModel):
    class_name: Literal["TemplateSection"]
    fileios: List[FileIOUnion] = Field(
        default=[],
        description=("List of fileio to include in the section.")
    )
    extensions: List[ExtensionUnion] = Field(
        default=[],
        description=("List of extensions to include in the section.")
    )
    groups: List[GroupUnion] = Field(
        default=[],
        description=("List of groups to include in the section.")
    )
    instructions: List[InstructionUnion] = Field(
        default=[],
        description=("List of instructions to include in the section.")
    )

    class Config:
        title = "TemplateSection"
        json_schema_extra = {
            "description": ("Base class for a templace section with its associated "
                            "groups, instructions, fileio, extensions and post-extensions.")
        }

class MinimizeTemplateModel(TemplateSectionModel):
    class_name: Literal["MinimizeTemplate"]
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
    use_anchors: bool = Field(
        default=False,
        description=("Whether to use anchors during the minimization.")
    )
    anchor_group: GroupUnion = Field(
        description=("Group to use for the anchors if use_anchors is True.")
    )

    class Config:
        title = "MinimizeTemplate"
        json_schema_extra = {
            "description": ("Perform an energy minimization of the system, by iteratively adjusting"
                            " atom coordinates. Iterations are terminated when one of the stopping "
                            "criteria is satisfied. If use_anchors is True, the anchor_group will" 
                            " be used and the force vectors of the atoms in the anchor_group will "
                            " be fixed to 0 during the minimization. "
                            "Lammps documentation: https://docs.lammps.org/minimize.html")
        }

class RecursiveSectionModel(SectionModel):
    class_name: Literal["RecursiveSection"]
    sections: List[TemplateUnion] = Field(
        default=[],
        description=("List of sections to include in the RecursiveSection.")
    )
    fileios: List[FileIOUnion] = Field(
        default=[],
        description=("List of fileio to include in the section.")
    )
    extensions: List[ExtensionUnion] = Field(
        default=[],
        description=("List of extensions to include in the section.")
    )
    groups: List[GroupUnion] = Field(
        default=[],
        description=("List of groups to include in the section.")
    )
    instructions: List[InstructionUnion] = Field(
        default=[],
        description=("List of instructions to include in the section.")
    )

    class Config:
        title = "RecursiveSection"
        json_schema_extra = {
            "description": ("A RecusiveSection declares a list of groups, instructions, fileio, "
                            "extensions and post-extensions which will be declared before the "
                            "execuion of a list of sub sections.")
        }

TemplateUnion = Annotated[ Union[
    MinimizeTemplateModel,
    RecursiveSectionModel,
    IntegratorSectionModel,
    InstructionsSectionModel],
    Field(discriminator="class_name")]
