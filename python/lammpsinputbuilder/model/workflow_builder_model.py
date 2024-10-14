from typing import List, Literal
from pydantic import BaseModel, Field

from lammpsinputbuilder.model.template_model import TemplateUnion
from lammpsinputbuilder.model.typedmolecule_model import TypedMolecularSystemUnion

class HeaderModel(BaseModel):
    major_version: int = Field(
        description=("Major version of the schema.")
    )
    minor_version: int = Field(
        description=("Minor version of the schema.")
    )
    format: Literal["WorkflowBuilder"]

    class Config:
        title = "Header"

        json_schema_extra = {
            "description": ("Header of the schema.")
        }

class WorkflowBuilderModel(BaseModel):
    header: HeaderModel = Field(
        description=("Header of the schema.")
    )
    sections: List[TemplateUnion] = Field(
        default=[],
        description=("List of sections to execute during the workflow.")
    )
    molecular_system: TypedMolecularSystemUnion = Field(
        description=("Molecular system used for the workflow.")
    )

    class Config:
        title = "WorkflowBuilder"

        json_schema_extra = {
            "description": ("Root object of a workflow. The WorkflowBuilder contains "
                            " a header defining the schema, a base molecular system, "
                            "and a sequence of sections to execute. "
                            "Documentation for the different objects: "
                            "https://github.com/madreher/LammpsInputBuilder")
        }
