from typing import List, Literal

from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.model.template_model import TemplateUnion
from lammpsinputbuilder.model.typedmolecule_model import TypedMolecularSystemUnion

class HeaderModel(BaseObjectModel):
    major_version: int
    minor_version: int
    format: str

class WorkflowBuilderModel(BaseObjectModel):
    class_name: Literal["WorkflowBuilder"]
    header: HeaderModel
    sections: List[TemplateUnion] = []
    molecular_system: TypedMolecularSystemUnion
