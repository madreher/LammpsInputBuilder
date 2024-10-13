from typing import List, Union, Annotated, Literal
from pydantic import Field

from lammpsinputbuilder.model.base_model import BaseObjectModel
from lammpsinputbuilder.fileio import DumpStyle

class FileIOModel(BaseObjectModel):
    pass

class DumpTrajectoryModel(FileIOModel):
    class_name: Literal["DumpTrajectoryFileIO"]
    user_fields: List[str] = Field(
        default=[],
        description=("List of fields to include in the dump trajectory file. "
                      "Settings only used if the dump style is set to custom.")
    )
    add_default_fields: bool = Field(
        description=("Add the default fields to the dump trajectory file. "
                      "Settings only used if the dump style is set to custom.")
    )
    interval: int = Field(
        description=("The trajectory file will be written every n time steps.")
    )
    group_name: str = Field(
        description=("Name of a group to apply the fileio to. "
                     "The given group must exist. "
                     "If not set, the fileio is applied to the \"all\" group."),
    )
    style: DumpStyle = Field(
        description=("The style of the dump trajectory file. "
                     "This method only supports \"custom\" and \"xyz\" style. "
                     "For non supported styles, use the ManualFileIOModel. "
                     "Lammps documentation: https://docs.lammps.org/dump.html"),
    )

    class Config:
        title = "DumpTrajectoryFileIO"
        json_schema_extra = {
            "description": ("Writes trajectory files in custom and xyz styles. "
                            "Lammps documentation: https://docs.lammps.org/dump.html")
        }

class ReaxBondFileIOModel(FileIOModel):
    class_name: Literal["ReaxBondFileIO"]
    group_name: str = Field(
        description=("Name of a group to apply the fileio to. "
                     "The given group must exist. "
                     "If not set, the fileio is applied to the \"all\" group."),
    )
    interval: int = Field(
        description=("The trajectory file will be written every n time steps.")
    )

    class Config:
        title = "ReaxBondFileIO"
        json_schema_extra = {
            "description": ("Writes trajectory files for the reax bonds. "
                            "Lammps documentation: https://docs.lammps.org/fix_reaxff_bonds.html")
        }

class ThermoFileIOModel(FileIOModel):
    class_name: Literal["ThermoFileIO"]
    interval: int = Field(
        description=("The trajectory file will be written every n time steps.")
    )
    user_fields: List[str] = Field(
        default=[],
        description=("List of fields to include in the thermo output. ")
    )
    add_default_fields: bool = Field(
        description=("Add the default fields to the thermo trajectory file."
                     " Default fields are function of the type of forcefield used.")
    )

    class Config:
        title = "ThermoFileIO"
        json_schema_extra = {
            "description": ("Modify the output of thermo."
                            "Lammps documentation: - https://docs.lammps.org/thermo_style.html"
                            "- https://docs.lammps.org/thermo_modify.html "
                            "- https://docs.lammps.org/thermo.html")
        }

class ManualFileIOModel(FileIOModel):
    class_name: Literal["ManualFileIO"]
    do_cmd: str = Field(
        description=("The Lammps command(s) to execute when the add_do_commands method is called. "
                    "The field can contain multiple commands separated by newlines.")
    )
    undo_cmd: str = Field(
        description=("The Lammps command(s) to execute when the add_undo_commands method is called."
                    " The field can contain multiple commands separated by newlines.")
    )
    associated_file_path: str = Field(
        description=("The file path of the file being produced by the fileio. ",
                     "Typically would return the filename of the trajectory file "
                     "produced in the job folder.")
    )

FileIOUnion = Annotated[Union[
    DumpTrajectoryModel,
    ReaxBondFileIOModel,
    ThermoFileIOModel,
    ManualFileIOModel
    ], Field(discriminator="class_name")]
