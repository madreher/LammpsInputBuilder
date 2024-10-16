"""Module implementing the quantity mecanics to convert units."""

from __future__ import annotations
from importlib.resources import files
from enum import IntEnum

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


class LammpsUnitSystem(IntEnum):
    REAL = 0
    METAL = 1

# TODO: move the expected_dimensionality to a static member of the class


class LIBQuantity():
    """
    Base class for all quantities. A LIBQuantity object is a wrapper around a pint Quantity object.
    Its goal is three fold:
    1. Hide the underlying pint Quantity object from the user.
    2. Add support for dimensionality checking.
    3. Support on demand conversion to different units.

    This class should never be instantiated directly. Instead, the subclasses 
    should implement the 'convert_to()' method.

    For convinience, in addition of the support of natural units provided by the users, LIB also 
    register Lammps units in the pint registry for the metal and real unit (https://docs.lammps.org/units.html)
    These units can be accessed with the name conventions "lmp_real_[units]" and "lmp_metal_[units]".
    For example: "lmp_real_velocity" or "lmp_metal_velocity". The available units are mass, length, time, 
    energy, velocity, force, torque and temperature.


    """
    def __init__(self, magnitude: float, units: str = "") -> None:
        """
        Constructor.
        Args:
            magnitude (float): The magnitude of the quantity
            units (str): The units of the quantity
        """
        self.magnitude = magnitude
        self.units = units
        self.quantity = magnitude * ureg(units)
        self.expected_dimensionality = [""]

    def get_magnitude(self) -> float:
        """
        Get the magnitude of the quantity
        Returns:
            float: The magnitude of the quantity
        """
        return self.magnitude

    def get_units(self) -> str:
        """
        Get the units of the quantity
        Returns:
            str: The units of the quantity
        """
        return self.units

    def validate_dimensionality(self) -> bool:
        """
        Validate the dimensionality of the quantity

        Raise:
            ValueError: If the dimensionality is not valid
        """
        if self.quantity.dimensionality not in self.expected_dimensionality:
            raise ValueError(
                (f"Expected dimensionality of {self.expected_dimensionality }, "
                f"got {self.quantity.dimensionality}."))

    def is_valid_unit(self, unit: str) -> bool:
        """
        Check if the unit is valid
        Args:
            unit (str): The unit to check
        Returns:
            bool: True if the unit is valid, False otherwise
        """
        #del unit
        #raise NotImplementedError(f"is_valid_unit not implemented for {__class__}")
        proxy = 0.0 * ureg(unit)
        return proxy.dimensionality in self.expected_dimensionality

    def to_dict(self) -> dict:
        """
        Get the dictionary representation of the quantity
        Returns:
            dict: The dictionary representation of the quantity
        """
        result = {}
        result["class_name"] = self.__class__.__name__
        result["magnitude"] = self.magnitude
        result["units"] = self.units
        return result

    def from_dict(self, d: dict, version: int) -> None:
        """
        Set the quantity from a dictionary
        Args:
            d (dict): The dictionary representation of the quantity
            version (int): The version of the dictionary
        """
        del version  # unused
        self.magnitude = d["magnitude"]
        self.units = d["units"]
        self.quantity = self.magnitude * ureg(self.units)

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit. Not implemented in LIBQuantity, 
        it must be implemented in the subclasses.
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class ForceQuantity(LIBQuantity):
    """
    Quantity object to represent a force. The force dimensionality is [mass] * [length] / [time] ** 2 / [substance]
    or [mass] * [length] / [time] ** 2
    """

    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_force") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = [
            "[mass] * [length] / [time] ** 2 / [substance]",
            "[mass] * [length] / [time] ** 2"
        ]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the force quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the force quantity
            version (int): The version of the force quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_force).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_force).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class TemperatureQuantity(LIBQuantity):
    """
    Quantity object to represent a temperature. The temperature dimensionality is [temperature]
    """
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_temperature") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = ["[temperature]"]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the temperature quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the temperature quantity
            version (int): The version of the temperature quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_temperature).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_temperature).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class TorqueQuantity(LIBQuantity):
    """
    Quantity object to represent a torque. The torque dimensionality is [mass] * [length] ** 2 / [time] ** 2 / [substance]
    or [mass] * [length] ** 2 / [time] ** 2
    """
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_torque") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = [
            "[mass] * [length] ** 2 / [time] ** 2 / [substance]",
            "[mass] * [length] ** 2 / [time] ** 2"
        ]
        self.validate_dimensionality()

    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the torque quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the torque quantity
            version (int): The version of the torque quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_torque).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_torque).magnitude

        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class TimeQuantity(LIBQuantity):
    """
    Quantity object to represent time. The time dimensionality is [time]
    """
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_time") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = ["[time]"]
        self.validate_dimensionality()


    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the time quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the time quantity
            version (int): The version of the time quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_time).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_time).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class EnergyQuantity(LIBQuantity):
    """
    Quantity object to represent energy. The energy dimensionality is [mass] * [length] ** 2 / [time] ** 2 / [substance]
    or [mass] * [length] ** 2 / [time] ** 2
    """
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_energy") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = [
            "[mass] * [length] ** 2 / [time] ** 2 / [substance]",
            "[mass] * [length] ** 2 / [time] ** 2"
        ]
        self.validate_dimensionality()


    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the energy quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the energy quantity
            version (int): The version of the energy quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_energy).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_energy).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class LengthQuantity(LIBQuantity):
    """
    Quantity object to represent length. The length dimensionality is [length].
    """
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_length") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = ["[length]"]
        self.validate_dimensionality()


    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the length quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the length quantity
            version (int): The version of the length quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_length).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_length).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")


class VelocityQuantity(LIBQuantity):
    """
    Quantity object to represent velocity. The velocity dimensionality is [length] / [time].
    """
    def __init__(
            self,
            value: float = 0.0,
            units: str = "lmp_real_velocity") -> None:
        """
        Constructor.
        Args:
            value (float): The magnitude of the quantity
            units (str): The units of the quantity
        Raise:
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        super().__init__(value, units)
        self.expected_dimensionality = ["[length] / [time]"]
        self.validate_dimensionality()


    def from_dict(self, d: dict, version: int) -> None:
        """
        Load the velocity quantity from a dictionary representation.
        Args:
            d (dict): The dictionary representation of the velocity quantity
            version (int): The version of the velocity quantity
        Raise:
            ValueError: If the class name in the dictionary does not match the class name of the object
            ValueError: If the dimensionality of the unit parameter does not match the expected dimensionality
        """
        class_name = d.get("class_name", "")
        if class_name != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {class_name}.")
        super().from_dict(d, version=version)
        self.validate_dimensionality()

    def convert_to(self, lmp_unit: LammpsUnitSystem) -> float:
        """
        Convert the quantity to a different unit
        Args:
            lmp_unit (LammpsUnitSystem): The unit system to convert to
        Returns:
            float: The magnitude of the quantity in the new unit
        Raise:
            NotImplementedError: If the unit system is not supported
        """
        if lmp_unit == LammpsUnitSystem.REAL:
            return self.quantity.to(ureg.lmp_real_velocity).magnitude
        if lmp_unit == LammpsUnitSystem.METAL:
            return self.quantity.to(ureg.lmp_metal_velocity).magnitude
        raise NotImplementedError(
            f"Lammps unit system {lmp_unit} not supported by class {__class__}")
