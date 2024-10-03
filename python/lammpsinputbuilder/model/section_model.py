from typing import List, Literal
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.group_model import GroupModel
from lammpsinputbuilder.model.instruction_model import InstructionModel
from lammpsinputbuilder.model.extension_model import ExtensionModel
from lammpsinputbuilder.model.fileio_model import FileIOModel
from lammpsinputbuilder.model.integrator_model import IntegratorModel

class SectionModel(BaseObjectModel):
    pass

class IntegratorSectionModel(SectionModel):
    class_name: Literal["IntegratorSection"]
    groups: List[GroupModel] = []
    instructions: List[InstructionModel] = []
    fileios: List[FileIOModel] = []
    extensions: List[ExtensionModel] = []
    integrator: IntegratorModel

class InstructionSectionModel(SectionModel):
    class_name: Literal["InstructionSection"]
    instructions: List[InstructionModel] = []