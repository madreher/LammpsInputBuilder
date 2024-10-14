from pydantic import BaseModel, Field

class LIBQuantityModel(BaseModel):
    magnitude: float = Field(
        description=("Magnitude of the quantity.")
    )
    units: str = Field(
        description=("Units of the quantity.")
    )

    class Config:
        title = "LIBQuantity"
        json_schema_extra = {
            "description": ("Base class for all quantity types.")
        }

class ForceQuantityModel(LIBQuantityModel):
    class_name: str = "ForceQuantity"

    class Config:
        title = "ForceQuantity"
        json_schema_extra = {
            "description": ("Force quantity. "
                            "The unit dimension has to be "
                            "[mass] * [length] / [time] ** 2 / [substance] or "
                            "[mass] * [length] / [time] ** 2")
        }

class TemperatureQuantityModel(LIBQuantityModel):
    class_name: str = "TemperatureQuantity"

    class Config:
        title = "TemperatureQuantity"
        json_schema_extra = {
            "description": ("Temperature quantity. "
                            "The unit dimension has to be [temperature]")
        }

class TorqueQuantityModel(LIBQuantityModel):
    class_name: str = "TorqueQuantity"

    class Config:
        title = "TorqueQuantity"
        json_schema_extra = {
            "description": ("Torque quantity. "
                            "The unit dimension has to be "
                            "[mass] * [length] ** 2 / [time] ** 2 / [substance] or "
                            "[mass] * [length] ** 2 / [time] ** 2")
        }

class TimeQuantityModel(LIBQuantityModel):
    class_name: str = "TimeQuantity"

    class Config:
        title = "TimeQuantity"
        json_schema_extra = {
            "description": ("Time quantity. "
                            "The unit dimension has to be [time]")
        }

class EnergyQuantityModel(LIBQuantityModel):
    class_name: str = "EnergyQuantity"

    class Config:
        title = "EnergyQuantity"
        json_schema_extra = {
            "description": ("Energy quantity. "
                            "The unit dimension has to be "
                            "[mass] * [length] ** 2 / [time] ** 2 / [substance] or "
                            "[mass] * [length] ** 2 / [time] ** 2")
        }

class LengthQuantityModel(LIBQuantityModel):
    class_name: str = "LengthQuantity"

    class Config:
        title = "LengthQuantity"
        json_schema_extra = {
            "description": ("Length quantity. "
                            "The unit dimension has to be [length]")
        }

class VelocityQuantityModel(LIBQuantityModel):
    class_name: str = "VelocityQuantity"

    class Config:
        title = "VelocityQuantity"
        json_schema_extra = {
            "description": ("Velocity quantity. "
                            "The unit dimension has to be [length] / [time]")
        }
