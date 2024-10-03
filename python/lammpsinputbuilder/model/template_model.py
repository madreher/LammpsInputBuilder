from __future__ import annotations
from typing import List, Union, Literal, Annotated
from pydantic import Field
from lammpsinputbuilder.model.section_model import SectionModel, \
    IntegratorSectionModel, InstructionSectionModel
from lammpsinputbuilder.model.fileio_model import FileIOUnion
from lammpsinputbuilder.model.group_model import GroupUnion
from lammpsinputbuilder.model.extension_model import ExtensionUnion
from lammpsinputbuilder.model.instruction_model import InstructionUnion

class TemplateSectionModel(SectionModel):
    class_name: Literal["TemplateSection"]
    fileios: List[FileIOUnion] = []
    extensions: List[ExtensionUnion] = []
    groups: List[GroupUnion] = []
    instructions: List[InstructionUnion] = []

class MinimizeTemplateModel(TemplateSectionModel):
    class_name: Literal["MinimizeTemplateSection"]
    style: int
    etol: float
    ftol: float
    maxiter: int
    maxeval: int
    use_anchors: bool
    anchor_group: GroupUnion

class RecursiveSectionModel(SectionModel):
    class_name: Literal["RecursiveSection"]
    sections: List[TemplateUnion] = []
    fileios: List[FileIOUnion] = []
    extensions: List[ExtensionUnion] = []
    groups: List[GroupUnion] = []
    instructions: List[InstructionUnion] = []

TemplateUnion = Annotated[ Union[
    MinimizeTemplateModel,
    RecursiveSectionModel,
    IntegratorSectionModel,
    InstructionSectionModel],
    Field(discriminator="class_name")]
