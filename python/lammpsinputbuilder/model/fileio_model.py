from typing import List, Union, Annotated, Literal
from pydantic import Field

from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.fileio import DumpStyle

class FileIOModel(BaseObjectModel):
    pass

class DumpTrajectoryModel(FileIOModel):
    class_name: Literal["DumpTrajectoryFileIO"]
    user_fields: List[str] = []
    add_default_fields: bool
    interval: int
    group_name: str
    style: DumpStyle

class ReaxBondFileIOModel(FileIOModel):
    class_name: Literal["ReaxBondFileIO"]
    group_name: str
    interval: int

class ThermoFileIOModel(FileIOModel):
    class_name: Literal["ThermoFileIO"]
    interval: int
    user_fields: List[str] = []
    add_default_fields: bool

class ManualFileIOModel(FileIOModel):
    class_name: Literal["ManualFileIO"]
    do_cmd: str
    undo_cmd: str
    associated_file_path: str

FileIOUnion = Annotated[Union[
    DumpTrajectoryModel,
    ReaxBondFileIOModel,
    ThermoFileIOModel,
    ManualFileIOModel
    ], Field(discriminator="class_name")]
