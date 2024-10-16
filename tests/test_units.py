import pytest 

from lammpsinputbuilder.quantities import *

def test_LengthQuantityDeclarations():
    lengthQuantity = LengthQuantity(1.0, "angstrom")
    assert lengthQuantity.get_magnitude() == 1.0
    assert lengthQuantity.get_units() == "angstrom"
    assert lengthQuantity.is_valid_unit("angstrom") is True
    assert lengthQuantity.is_valid_unit("s") is False

    dict_result = lengthQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "angstrom"
    assert dict_result["class_name"] == "LengthQuantity"

    loadBackQuantity = LengthQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "angstrom"

    lengthRealUnit = LengthQuantity(1.0, "lmp_real_length")
    assert lengthRealUnit.get_magnitude() == 1.0
    assert lengthRealUnit.get_units() == "lmp_real_length"
    
    assert lengthRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert lengthRealUnit.convert_to(LammpsUnitSystem.METAL) == 1.0

    lengthMetalUnit = LengthQuantity(1.0, "lmp_metal_length")
    assert lengthMetalUnit.get_magnitude() == 1.0
    assert lengthMetalUnit.get_units() == "lmp_metal_length"

    assert lengthMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert lengthMetalUnit.convert_to(LammpsUnitSystem.REAL) == 1.0

    with pytest.raises(ValueError):
        failedLength = LengthQuantity(1.0, "A") # Wrong unit

    

def test_TimeQuantityDeclarations():
    timeQuantity = TimeQuantity(1.0, "ps")
    assert timeQuantity.get_magnitude() == 1.0
    assert timeQuantity.get_units() == "ps"
    assert timeQuantity.is_valid_unit("s") is True
    assert timeQuantity.is_valid_unit("bohr") is False

    dict_result = timeQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "ps"
    assert dict_result["class_name"] == "TimeQuantity"

    loadBackQuantity = TimeQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "ps"

    timeRealUnit = TimeQuantity(1.0, "lmp_real_time")
    assert timeRealUnit.get_magnitude() == 1.0
    assert timeRealUnit.get_units() == "lmp_real_time"

    assert timeRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert timeRealUnit.convert_to(LammpsUnitSystem.METAL) == pytest.approx(0.001)

    timeMetalUnit = TimeQuantity(1.0, "lmp_metal_time")
    assert timeMetalUnit.get_magnitude() == 1.0
    assert timeMetalUnit.get_units() == "lmp_metal_time"

    assert timeMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert timeMetalUnit.convert_to(LammpsUnitSystem.REAL) == pytest.approx(1000.0) 

    with pytest.raises(ValueError):
        failedTime = TimeQuantity(1.0, "m")

def test_VelocityQuantityDeclarations():
    velocityQuantity = VelocityQuantity(1.0, "m/s")
    assert velocityQuantity.get_magnitude() == 1.0
    assert velocityQuantity.get_units() == "m/s"
    assert velocityQuantity.is_valid_unit("angstrom/s") is True
    assert velocityQuantity.is_valid_unit("bohr") is False

    dict_result = velocityQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "m/s"
    assert dict_result["class_name"] == "VelocityQuantity"

    loadBackQuantity = VelocityQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "m/s"

    velocityRealUnit = VelocityQuantity(1.0, "lmp_real_velocity")
    assert velocityRealUnit.get_magnitude() == 1.0
    assert velocityRealUnit.get_units() == "lmp_real_velocity"

    assert velocityRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert velocityRealUnit.convert_to(LammpsUnitSystem.METAL) == pytest.approx(1000.0)

    velocityMetalUnit = VelocityQuantity(1.0, "lmp_metal_velocity")
    assert velocityMetalUnit.get_magnitude() == 1.0
    assert velocityMetalUnit.get_units() == "lmp_metal_velocity"

    assert velocityMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert velocityMetalUnit.convert_to(LammpsUnitSystem.REAL) == pytest.approx(0.001, 1e-3)

    with pytest.raises(ValueError):
        failedVelocity = VelocityQuantity(1.0, "m")

def test_EnergyQuantityDeclarations():
    energyQuantity = EnergyQuantity(1.0, "kcal/mol")
    assert energyQuantity.get_magnitude() == 1.0
    assert energyQuantity.get_units() == "kcal/mol"
    assert energyQuantity.is_valid_unit("eV") is True
    assert energyQuantity.is_valid_unit("bohr") is False

    dict_result = energyQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "kcal/mol"
    assert dict_result["class_name"] == "EnergyQuantity"

    loadBackQuantity = EnergyQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "kcal/mol"

    energyRealUnit = EnergyQuantity(1.0, "lmp_real_energy")
    assert energyRealUnit.get_magnitude() == 1.0
    assert energyRealUnit.get_units() == "lmp_real_energy"

    # Conversion table: http://wild.life.nctu.edu.tw/class/common/energy-unit-conv-table-detail.html
    assert energyRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert energyRealUnit.convert_to(LammpsUnitSystem.METAL) == pytest.approx(0.0433634, 1e-3)

    energyMetalUnit = EnergyQuantity(1.0, "lmp_metal_energy")
    assert energyMetalUnit.get_magnitude() == 1.0
    assert energyMetalUnit.get_units() == "lmp_metal_energy"

    assert energyMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert energyMetalUnit.convert_to(LammpsUnitSystem.REAL) == pytest.approx(23.0609, 1e-3)

    with pytest.raises(ValueError):
        failedEnergy = EnergyQuantity(1.0, "m")

def test_TemperatureQuantityDeclarations():
    temperatureQuantity = TemperatureQuantity(1.0, "K")
    assert temperatureQuantity.get_magnitude() == 1.0
    assert temperatureQuantity.get_units() == "K"
    assert temperatureQuantity.is_valid_unit("K") is True
    assert temperatureQuantity.is_valid_unit("bohr") is False

    dict_result = temperatureQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "K"
    assert dict_result["class_name"] == "TemperatureQuantity"

    loadBackQuantity = TemperatureQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "K"

    temperatureRealUnit = TemperatureQuantity(1.0, "lmp_real_temperature")
    assert temperatureRealUnit.get_magnitude() == 1.0
    assert temperatureRealUnit.get_units() == "lmp_real_temperature"

    assert temperatureRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert temperatureRealUnit.convert_to(LammpsUnitSystem.METAL) == pytest.approx(1.0, 1e-3)

    temperatureMetalUnit = TemperatureQuantity(1.0, "lmp_metal_temperature")
    assert temperatureMetalUnit.get_magnitude() == 1.0
    assert temperatureMetalUnit.get_units() == "lmp_metal_temperature"

    assert temperatureMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert temperatureMetalUnit.convert_to(LammpsUnitSystem.REAL) == pytest.approx(1.0, 1e-3)

    with pytest.raises(ValueError):
        failedTemperature = TemperatureQuantity(1.0, "m")

def test_ForceQuantityDeclarations():
    forceQuantity = ForceQuantity(1.0, "kcal/mol/angstrom")
    assert forceQuantity.get_magnitude() == 1.0
    assert forceQuantity.get_units() == "kcal/mol/angstrom"
    assert forceQuantity.is_valid_unit("kcal/mol/angstrom") is True
    assert forceQuantity.is_valid_unit("bohr") is False

    dict_result = forceQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "kcal/mol/angstrom"
    assert dict_result["class_name"] == "ForceQuantity"

    loadBackQuantity = ForceQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "kcal/mol/angstrom"

    forceRealUnit = ForceQuantity(1.0, "lmp_real_force")
    assert forceRealUnit.get_magnitude() == 1.0
    assert forceRealUnit.get_units() == "lmp_real_force"

    assert forceRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert forceRealUnit.convert_to(LammpsUnitSystem.METAL) == pytest.approx(0.0433634, 1e-3)

    forceMetalUnit = ForceQuantity(1.0, "lmp_metal_force")
    assert forceMetalUnit.get_magnitude() == 1.0
    assert forceMetalUnit.get_units() == "lmp_metal_force"

    assert forceMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert forceMetalUnit.convert_to(LammpsUnitSystem.REAL) == pytest.approx(23.0609, 1e-3)

    with pytest.raises(ValueError):
        failedForce = ForceQuantity(1.0, "m")

def test_TorqueQuantityDeclarations():
    torqueQuantity = TorqueQuantity(1.0, "kcal/mol")
    assert torqueQuantity.get_magnitude() == 1.0
    assert torqueQuantity.get_units() == "kcal/mol"
    assert torqueQuantity.is_valid_unit("kcal/mol") is True
    assert torqueQuantity.is_valid_unit("bohr") is False

    dict_result = torqueQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "kcal/mol"
    assert dict_result["class_name"] == "TorqueQuantity"

    loadBackQuantity = TorqueQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.get_magnitude() == 1.0
    assert loadBackQuantity.get_units() == "kcal/mol"

    torqueRealUnit = TorqueQuantity(1.0, "lmp_real_torque")
    assert torqueRealUnit.get_magnitude() == 1.0
    assert torqueRealUnit.get_units() == "lmp_real_torque"

    assert torqueRealUnit.convert_to(LammpsUnitSystem.REAL) == 1.0
    assert torqueRealUnit.convert_to(LammpsUnitSystem.METAL) == pytest.approx(0.0433634, 1e-3)

    torqueMetalUnit = TorqueQuantity(1.0, "lmp_metal_torque")
    assert torqueMetalUnit.get_magnitude() == 1.0
    assert torqueMetalUnit.get_units() == "lmp_metal_torque"

    assert torqueMetalUnit.convert_to(LammpsUnitSystem.METAL) == 1.0
    assert torqueMetalUnit.convert_to(LammpsUnitSystem.REAL) == pytest.approx(23.0609, 1e-3)

    with pytest.raises(ValueError):
        failedTorque = TorqueQuantity(1.0, "m")

    

if __name__ == "__main__":
    test_LengthQuantityDeclarations()

