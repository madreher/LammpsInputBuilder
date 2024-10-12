from pydantic import BaseModel, Field

class BaseObjectModel(BaseModel):
    id_name: str = Field(
        pattern="[a-zA-Z_][a-zA-Z0-9_]*",
        description="Name of the object. Used as ID when generating the Lammps commands.")
