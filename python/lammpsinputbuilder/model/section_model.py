from typing import List, Literal
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
    groups: List[GroupUnion] = []
    instructions: List[InstructionUnion] = []
    fileios: List[FileIOUnion] = []
    extensions: List[ExtensionUnion] = []
    integrator: IntegratorUnion

class InstructionsSectionModel(SectionModel):
    class_name: Literal["InstructionsSection"]
    instructions: List[InstructionUnion] = []