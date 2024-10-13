from typing import List, Union, Annotated, Literal
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.group import OperationGroupEnum

class GroupModel(BaseObjectModel):
    pass

class IndicesGroupModel(GroupModel):
    class_name: Literal["IndicesGroup"]
    indices:List[int] = Field(
        description=("List of 1-based atom IDs belonging to the group.")
    )

    class Config:
        title = "IndicesGroup"
        json_schema_extra = {
            "description": ("Select a list of atoms by their atom indices. "
                            "Indices start at 1."
                            "Lammps documentation: https://docs.lammps.org/group.html")
        }

class AllGroupModel(GroupModel):
    class_name: Literal["AllGroup"]

    class Config:
        title = "AllGroup"
        json_schema_extra = {
            "description": ("Group object for the default \"all\" group. "
                            "Lammps documentation: https://docs.lammps.org/group.html")
        }

class EmptyGroupModel(GroupModel):
    class_name: Literal["EmptyGroup"]

    class Config:
        title = "EmptyGroup"
        json_schema_extra = {
            "description": ("Group object for the empty group. "
                            "Lammps documentation: https://docs.lammps.org/group.html")
        }

class OperationGroupModel(GroupModel):
    class_name: Literal["OperationGroup"]
    op: OperationGroupEnum
    other_groups_name: List[str] = Field(
        description=("List of other groups to apply the operation to. "
                     "All the group names must be declared prior to this group. "
                     "Lammps documentation: https://docs.lammps.org/group.html")
    )

    class Config:
        title = "OperationGroup"
        json_schema_extra = {
            "description": (
                    "Group object created from an operation on other groups. "
                    "Operation currently supported are substract, union, and intersect. "
                    "For non supported operation or other grouping style, use the ManualGroupModel."
                    " Lammps documentation: https://docs.lammps.org/group.html")
        }

class ReferenceGroupModel(GroupModel):
    class_name: Literal["ReferenceGroup"]
    reference_name: str = Field(
        description=("Name of a group to point to. The reference group must exist.")
    )

    class Config:
        title = "ReferenceGroup"
        json_schema_extra = {
            "description": ("Group object that points to another group. "
                            "The referenced group must exist. "
                            "This group doesn't create or delete a new group."
                            "Lammps documentation: https://docs.lammps.org/group.html")
        }

class ManualGroupModel(GroupModel):
    class_name: Literal["ManualGroup"]
    do_cmd: str = Field(
        description=("The Lammps command(s) to execute when the add_do_commands method is called. "
                     "The field can contain multiple commands separated by newlines.")
    )
    undo_cmd: str = Field(
        description=("The Lammps command(s) to execute when the add_undo_commands method is called."
                     " The field can contain multiple commands separated by newlines.")
    )

    class Config:
        title = "ManualGroup"
        json_schema_extra = {
            "description": ("Group object created by the user. "
                            "The user is responsible for writing the commands in the do_cmd and undo_cmd sections. "
                            "Note that no verifications can be done on the commands and are the"
                            " sole responsibility of the user."
                            "Lammps documentation: https://docs.lammps.org/group.html")
        }

GroupUnion = Annotated[Union[
    IndicesGroupModel,
    AllGroupModel,
    EmptyGroupModel,
    OperationGroupModel,
    ReferenceGroupModel,
    ManualGroupModel],
    Field(discriminator="class_name")]
