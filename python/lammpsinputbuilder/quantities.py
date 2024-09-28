"""Module implementing the quantity mecanics to convert units."""

from __future__ import annotations
from importlib.resources import files
from enum import Enum

import pint


# Global registry required to use pint automatically and add units directy
# into the registery
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


class LammpsUnitSystem(Enum):
    REAL = 0
    METAL = 1

# TODO: move the expected_dimensionality to a static member of the class


class LIBQuantity():
    def __init__(self, magnitude: float, units: str = "") -> None:
        self.magnitude = magnitude
        self.units = units
        self.quantity = magnitude * ureg(units)
        self.expected_dimensionality = [""]

    def get_magnitude(self) -> float:
        return self.magnitude

    def get_units(self) -> str:
        return self.units

    def validate_dimensionality(self) -> bool:
        if self.quantity.dimensionality not in self.expected_dimensionality:
            raise ValueError(
                (f"Expected dimensionality of {self.expected_dimensionality }, "
                f"got {self.quantity.dimensionality}."))
        return True

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["magnitude"] = self.magnitude
        result["units"] = self.units
        return result

    def from_dict(self, d: dict, version: int) -> None:
        del version  # unused
        self.magnitude = d["magnitude"]
        self.units = d["units"]
        self.quantity = self.magnitude * ureg(self.units)

    def get_value(self) -> float:
        return self.magnitude

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class ForceQuantity(LIBQuantity):

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_force") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = [
            "[mass] * [length] / [time] ** 2 / [substance]",
            "[mass] * [length] / [time] ** 2"
        ]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_force).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_force).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class TemperatureQuantity(LIBQuantity):

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_temperature") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = ["[temperature]"]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_temperature).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_temperature).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class TorqueQuantity(LIBQuantity):

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_torque") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = [
            "[mass] * [length] ** 2 / [time] ** 2 / [substance]",
            "[mass] * [length] ** 2 / [time] ** 2"
        ]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_torque).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_torque).magnitude

        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class TimeQuantity(LIBQuantity):

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_time") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = ["[time]"]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_time).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_time).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class EnergyQuantity(LIBQuantity):

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_energy") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = [
            "[mass] * [length] ** 2 / [time] ** 2 / [substance]",
            "[mass] * [length] ** 2 / [time] ** 2"
        ]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_energy).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_energy).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class LengthQuantity(LIBQuantity):
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_length") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = ["[length]"]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_length).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_length).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class VelocityQuantity(LIBQuantity):

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_velocity") -> None:
        super().__init__(value, units)
        self.expected_dimensionality = ["[length] / [time]"]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        class_name = d.get("class", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_velocity).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_velocity).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")
