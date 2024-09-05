from __future__ import annotations
from enum import Enum

import pint 
from importlib.resources import files

# Global registry required to use pint automatically and add units directy into the registery 
ureg = pint.UnitRegistry()
pint.set_application_registry(ureg)

# Add unit sets to the registry
unitsFilePath = files('lammpsinputbuilder').joinpath('units.txt')
ureg.load_definitions(str(unitsFilePath))
ureg.enable_contexts('lammpsinputbuilder')

# Define the real units
ureg.define("lmp_real_mass = grams / mole")
ureg.define("lmp_real_length = angstrom")
ureg.define("lmp_real_time = femtoseconds")
ureg.define("lmp_real_energy = kcal / mol")
ureg.define("lmp_real_velocity = angstrom / femtoseconds")
ureg.define("lmp_real_force = (kcal / mol) / angstrom")
ureg.define("lmp_real_torque = kcal / mol")
ureg.define("lmp_real_temperature = kelvin")

# Define the metal units 
ureg.define("lmp_metal_mass = grams / mole")
ureg.define("lmp_metal_length = angstrom")
ureg.define("lmp_metal_time = picoseconds")
ureg.define("lmp_metal_energy = eV")
ureg.define("lmp_metal_velocity = angstrom / picoseconds")
ureg.define("lmp_metal_force = eV / angstrom")
ureg.define("lmp_metal_torque = eV")
ureg.define("lmp_metal_temperature = kelvin")

# Define types of units 
class UnitType(Enum):
    MASS = 0,
    LENGTH = 1,
    TIME = 2,
    ENERGY = 3,
    VELOCITY = 4,
    FORCE = 5,
    TORQUE = 6,
    TEMPERATURE = 7

# Define default conversion tables
mapLammpsRealUnits = {
    UnitType.MASS: ureg.lmp_real_mass,
    UnitType.LENGTH: ureg.lmp_real_length,
    UnitType.TIME: ureg.lmp_real_time,
    UnitType.ENERGY: ureg.lmp_real_energy,
    UnitType.VELOCITY: ureg.lmp_real_velocity,
    UnitType.FORCE: ureg.lmp_real_force,
    UnitType.TORQUE: ureg.lmp_real_torque,
    UnitType.TEMPERATURE: ureg.lmp_real_temperature
}

mapLammpsMetalUnits = {
    UnitType.MASS: ureg.lmp_metal_mass,
    UnitType.LENGTH: ureg.lmp_metal_length,
    UnitType.TIME: ureg.lmp_metal_time,
    UnitType.ENERGY: ureg.lmp_metal_energy,
    UnitType.VELOCITY: ureg.lmp_metal_velocity,
    UnitType.FORCE: ureg.lmp_metal_force,
    UnitType.TORQUE: ureg.lmp_metal_torque,
    UnitType.TEMPERATURE: ureg.lmp_metal_temperature
}


class LIBQuantity():
    def __init__(self, magnitude: float, units: str = "") -> None:
        self.magnitude = magnitude
        self.units = units
        self.quantity = magnitude * ureg(units)

    def getMagnitude(self) -> float:
        return self.magnitude
    
    def getUnits(self) -> str:
        return self.units
    
    def checkDimensionality(self) -> bool:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["value"] = self.magnitude
        result["units"] = self.units
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        value = d["value"]
        unit = d["units"]
        self.quantity = value * ureg(unit)

    def getValue(self) -> float:
        return self.magnitude

    def convertTo(self, unit: str) -> LIBQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class TimeQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "") -> None:
        LIBQuantity.__init__(value, unitStr)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> TimeQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class ForceQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "") -> None:
        LIBQuantity.__init__(value, unitStr)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> ForceQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class TemperatureQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "") -> None:
        LIBQuantity.__init__(value, unitStr)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> TimeQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class TorqueQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "") -> None:
        LIBQuantity.__init__(value, unitStr)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> TorqueQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class TimeQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "") -> None:
       LIBQuantity.__init__(value, unitStr)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> TimeQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class EnergyQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "") -> None:
        LIBQuantity.__init__(value, unitStr)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> EnergyQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")

class DistanceQuantity(LIBQuantity):
    def __init__(self, value: float, unitStr: str = "") -> None:
        LIBQuantity.__init__(self, value, unitStr)
        if  not self.checkDimensionality():
            raise ValueError(f"Expected dimensionality of length, got {self.quantity.dimensionality}.")

    def checkDimensionality(self) -> bool:
        return self.quantity.dimensionality == "[length]"

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        if  not self.checkDimensionality():
            raise ValueError(f"Expected dimensionality of length, got {self.quantity.dimensionality}.")

    def convertTo(self, unit: str) -> DistanceQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")

class VelocityQuantity(LIBQuantity):

    def __init__(self, value: float, unitStr: str = "", units: pint.Unit = None) -> None:
        super().__init__(value, unitStr, units)

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)

    def convertTo(self, unit: str) -> VelocityQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")