import pytest 

from lammpsinputbuilder.quantities import *

def test_DistanceQuantityDeclarations():
    distanceQuantity = DistanceQuantity(1.0, "angstrom")
    assert distanceQuantity.getMagnitude() == 1.0
    assert distanceQuantity.getUnits() == "angstrom"

    distanceRealUnit = DistanceQuantity(1.0, "lmp_real_length")
    assert distanceRealUnit.getMagnitude() == 1.0
    assert distanceRealUnit.getUnits() == "lmp_real_length"

    distanceMetalUnit = DistanceQuantity(1.0, "lmp_metal_length")
    assert distanceMetalUnit.getMagnitude() == 1.0
    assert distanceMetalUnit.getUnits() == "lmp_metal_length"

    with pytest.raises(ValueError):
        failedDistance = DistanceQuantity(1.0, "A") # Wrong unit

def test_TimeQuantityDeclarations():
    timeQuantity = TimeQuantity(1.0, "ps")
    assert timeQuantity.getMagnitude() == 1.0
    assert timeQuantity.getUnits() == "ps"

    timeRealUnit = TimeQuantity(1.0, "lmp_real_time")
    assert timeRealUnit.getMagnitude() == 1.0
    assert timeRealUnit.getUnits() == "lmp_real_time"

    timeMetalUnit = TimeQuantity(1.0, "lmp_metal_time")
    assert timeMetalUnit.getMagnitude() == 1.0
    assert timeMetalUnit.getUnits() == "lmp_metal_time"

    with pytest.raises(ValueError):
        failedTime = TimeQuantity(1.0, "m")

def test_VelocityQuantityDeclarations():
    velocityQuantity = VelocityQuantity(1.0, "m/s")
    assert velocityQuantity.getMagnitude() == 1.0
    assert velocityQuantity.getUnits() == "m/s"

    velocityRealUnit = VelocityQuantity(1.0, "lmp_real_velocity")
    assert velocityRealUnit.getMagnitude() == 1.0
    assert velocityRealUnit.getUnits() == "lmp_real_velocity"

    velocityMetalUnit = VelocityQuantity(1.0, "lmp_metal_velocity")
    assert velocityMetalUnit.getMagnitude() == 1.0
    assert velocityMetalUnit.getUnits() == "lmp_metal_velocity"

    with pytest.raises(ValueError):
        failedVelocity = VelocityQuantity(1.0, "m")

def test_EnergyQuantityDeclarations():
    energyQuantity = EnergyQuantity(1.0, "kcal/mol")
    assert energyQuantity.getMagnitude() == 1.0
    assert energyQuantity.getUnits() == "kcal/mol"

    energyRealUnit = EnergyQuantity(1.0, "lmp_real_energy")
    assert energyRealUnit.getMagnitude() == 1.0
    assert energyRealUnit.getUnits() == "lmp_real_energy"

    energyMetalUnit = EnergyQuantity(1.0, "lmp_metal_energy")
    assert energyMetalUnit.getMagnitude() == 1.0
    assert energyMetalUnit.getUnits() == "lmp_metal_energy"

    with pytest.raises(ValueError):
        failedEnergy = EnergyQuantity(1.0, "m")

def test_TemperatureQuantityDeclarations():
    temperatureQuantity = TemperatureQuantity(1.0, "K")
    assert temperatureQuantity.getMagnitude() == 1.0
    assert temperatureQuantity.getUnits() == "K"

    temperatureRealUnit = TemperatureQuantity(1.0, "lmp_real_temperature")
    assert temperatureRealUnit.getMagnitude() == 1.0
    assert temperatureRealUnit.getUnits() == "lmp_real_temperature"

    temperatureMetalUnit = TemperatureQuantity(1.0, "lmp_metal_temperature")
    assert temperatureMetalUnit.getMagnitude() == 1.0
    assert temperatureMetalUnit.getUnits() == "lmp_metal_temperature"

    with pytest.raises(ValueError):
        failedTemperature = TemperatureQuantity(1.0, "m")

def test_ForceQuantityDeclarations():
    forceQuantity = ForceQuantity(1.0, "kcal/mol/angstrom")
    assert forceQuantity.getMagnitude() == 1.0
    assert forceQuantity.getUnits() == "kcal/mol/angstrom"

    forceRealUnit = ForceQuantity(1.0, "lmp_real_force")
    assert forceRealUnit.getMagnitude() == 1.0
    assert forceRealUnit.getUnits() == "lmp_real_force"

    forceMetalUnit = ForceQuantity(1.0, "lmp_metal_force")
    assert forceMetalUnit.getMagnitude() == 1.0
    assert forceMetalUnit.getUnits() == "lmp_metal_force"

    with pytest.raises(ValueError):
        failedForce = ForceQuantity(1.0, "m")

def test_TorqueQuantityDeclarations():
    torqueQuantity = TorqueQuantity(1.0, "kcal/mol")
    assert torqueQuantity.getMagnitude() == 1.0
    assert torqueQuantity.getUnits() == "kcal/mol"

    torqueRealUnit = TorqueQuantity(1.0, "lmp_real_torque")
    assert torqueRealUnit.getMagnitude() == 1.0
    assert torqueRealUnit.getUnits() == "lmp_real_torque"

    torqueMetalUnit = TorqueQuantity(1.0, "lmp_metal_torque")
    assert torqueMetalUnit.getMagnitude() == 1.0
    assert torqueMetalUnit.getUnits() == "lmp_metal_torque"

    with pytest.raises(ValueError):
        failedTorque = TorqueQuantity(1.0, "m")

if __name__ == "__main__":
    test_DistanceQuantityDeclarations()

