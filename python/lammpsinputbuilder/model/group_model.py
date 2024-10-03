from typing import List, Union, Annotated, Literal
from pydantic import Field
from lammpsinputbuilder.model.base_model import BaseObjectModel

class GroupModel(BaseObjectModel):
    pass

class IndicesGroupModel(GroupModel):
    class_name: Literal["IndicesGroup"]
    indices:List[int]

class AllGroupModel(GroupModel):
    class_name: Literal["AllGroup"]

class EmptyGroupModel(GroupModel):
    class_name: Literal["EmptyGroup"]

class OperationGroupModel(GroupModel):
    class_name: Literal["OperationGroup"]
    op: int
    other_groups_name: List[str]

class ReferenceGroupModel(GroupModel):
    class_name: Literal["ReferenceGroup"]
    reference_name: str

class ManualGroupModel(GroupModel):
    class_name: Literal["ManualGroup"]
    do_cmd: str
    undo_cmd: str

GroupUnion = Annotated[Union[
    IndicesGroupModel,
    AllGroupModel,
    EmptyGroupModel,
    OperationGroupModel,
    ReferenceGroupModel,
    ManualGroupModel],
    Field(discriminator="class_name")]
