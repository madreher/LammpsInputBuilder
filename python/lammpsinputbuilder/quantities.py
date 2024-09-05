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

class LammpsUnitSystem(Enum):
    REAL = 0,
    METAL = 1

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

# TODO: move the expectedDimensionality to a static member of the class

class LIBQuantity():
    def __init__(self, magnitude: float, units: str = "") -> None:
        self.magnitude = magnitude
        self.units = units
        self.quantity = magnitude * ureg(units)
        self.expectedDimensionality = [""]

    def getMagnitude(self) -> float:
        return self.magnitude
    
    def getUnits(self) -> str:
        return self.units
    
    def validateDimensionality(self) -> bool:
        if self.quantity.dimensionality not in self.expectedDimensionality:
            raise ValueError(f"Expected dimensionality of {self.expectedDimensionality }, got {self.quantity.dimensionality}.")
        return True
    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["magnitude"] = self.magnitude
        result["units"] = self.units
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        self.magnitude = d["magnitude"]
        self.units = d["units"]
        self.quantity = self.magnitude * ureg(self.units)

    def getValue(self) -> float:
        return self.magnitude

    def convertTo(self, unit: str) -> LIBQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class ForceQuantity(LIBQuantity):

    def __init__(self, value: float = 0.0, units: str = "lmp_real_force") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = [
            "[mass] * [length] / [time] ** 2 / [substance]",
            "[mass] * [length] / [time] ** 2"
            ]
        self.validateDimensionality()
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()

    def convertTo(self, lmpUnit:LammpsUnitSystem) -> float:
        if lmpUnit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_force).magnitude
        elif lmpUnit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_force).magnitude
        else:
            raise NotImplementedError(f"Lammps unit system {lmpUnit} not supported by class {__class__}")
    
class TemperatureQuantity(LIBQuantity):

    def __init__(self, value: float = 0.0, units: str = "lmp_real_temperature") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = ["[temperature]"]
        self.validateDimensionality()
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()

    def convertTo(self, lmpUnit:LammpsUnitSystem) -> float:
        if lmpUnit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_time).magnitude
        elif lmpUnit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_time).magnitude
        else:
            raise NotImplementedError(f"Lammps unit system {lmpUnit} not supported by class {__class__}")
    
class TorqueQuantity(LIBQuantity):

    def __init__(self, value: float = 0.0, units: str = "lmp_real_torque") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = [
            "[mass] * [length] ** 2 / [time] ** 2 / [substance]",
            "[mass] * [length] ** 2 / [time] ** 2"
            ]
        self.validateDimensionality()
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()

    def convertTo(self, unit: str) -> TorqueQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class TimeQuantity(LIBQuantity):

    def __init__(self, value: float = 0.0, units: str = "lmp_real_time") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = ["[time]"]
        self.validateDimensionality()
           
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()

    def convertTo(self, unit: str) -> TimeQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class EnergyQuantity(LIBQuantity):

    def __init__(self, value: float = 0.0, units: str = "lmp_real_energy") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = [
            "[mass] * [length] ** 2 / [time] ** 2 / [substance]",
            "[mass] * [length] ** 2 / [time] ** 2"
            ]
        self.validateDimensionality()
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()

    def convertTo(self, unit: str) -> EnergyQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")

class LengthQuantity(LIBQuantity):
    def __init__(self, value: float = 0.0, units: str = "lmp_real_length") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = ["[length]"]
        self.validateDimensionality()
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()
    def convertTo(self, unit: str) -> float:
        raise NotImplementedError(f"Method not implemented by class {__class__}")

class VelocityQuantity(LIBQuantity):

    def __init__(self, value: float = 0.0, units: str = "lmp_real_velocity") -> None:
        super().__init__(value, units)
        self.expectedDimensionality = ["[length] / [time]"]
        self.validateDimensionality()
    
    def fromDict(self, d: dict, version: int) -> None:
        className = d.get("class", "")
        if className != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {className}.")
        super().fromDict(d, version=version)
        self.validateDimensionality()

    def convertTo(self, unit: str) -> VelocityQuantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")