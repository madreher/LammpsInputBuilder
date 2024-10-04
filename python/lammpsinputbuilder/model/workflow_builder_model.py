from typing import List, Literal
from pydantic import BaseModel

from lammpsinputbuilder.model.template_model import TemplateUnion
from lammpsinputbuilder.model.typedmolecule_model import TypedMolecularSystemUnion

class HeaderModel(BaseModel):
    major_version: int
    minor_version: int
    format: Literal["WorkflowBuilder"]

class WorkflowBuilderModel(BaseModel):
    header: HeaderModel
    sections: List[TemplateUnion] = []
    molecular_system: TypedMolecularSystemUnion
