from pydantic import BaseModel

class LIBQuantityModel(BaseModel):
    magnitude: float
    units: str

class ForceQuantityModel(LIBQuantityModel):
    class_name: str = "ForceQuantity"

class TemperatureQuantityModel(LIBQuantityModel):
    class_name: str = "TemperatureQuantity"

class TorqueQuantityModel(LIBQuantityModel):
    class_name: str = "TorqueQuantity"

class TimeQuantityModel(LIBQuantityModel):
    class_name: str = "TimeQuantity"

class EnergyQuantityModel(LIBQuantityModel):
    class_name: str = "EnergyQuantity"

class LengthQuantityModel(LIBQuantityModel):
    class_name: str = "LengthQuantity"

class VelocityQuantityModel(LIBQuantityModel):
    class_name: str = "VelocityQuantity"

