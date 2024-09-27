import pytest 

from lammpsinputbuilder.quantities import *

def test_LengthQuantityDeclarations():
    lengthQuantity = LengthQuantity(1.0, "angstrom")
    assert lengthQuantity.getMagnitude() == 1.0
    assert lengthQuantity.getUnits() == "angstrom"

    dict_result = lengthQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "angstrom"
    assert dict_result["class"] == "LengthQuantity"

    loadBackQuantity = LengthQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "angstrom"

    lengthRealUnit = LengthQuantity(1.0, "lmp_real_length")
    assert lengthRealUnit.getMagnitude() == 1.0
    assert lengthRealUnit.getUnits() == "lmp_real_length"
    
    assert lengthRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert lengthRealUnit.convertTo(LammpsUnitSystem.METAL) == 1.0

    lengthMetalUnit = LengthQuantity(1.0, "lmp_metal_length")
    assert lengthMetalUnit.getMagnitude() == 1.0
    assert lengthMetalUnit.getUnits() == "lmp_metal_length"

    assert lengthMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert lengthMetalUnit.convertTo(LammpsUnitSystem.REAL) == 1.0

    with pytest.raises(ValueError):
        failedLength = LengthQuantity(1.0, "A") # Wrong unit

    

def test_TimeQuantityDeclarations():
    timeQuantity = TimeQuantity(1.0, "ps")
    assert timeQuantity.getMagnitude() == 1.0
    assert timeQuantity.getUnits() == "ps"

    dict_result = timeQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "ps"
    assert dict_result["class"] == "TimeQuantity"

    loadBackQuantity = TimeQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "ps"

    timeRealUnit = TimeQuantity(1.0, "lmp_real_time")
    assert timeRealUnit.getMagnitude() == 1.0
    assert timeRealUnit.getUnits() == "lmp_real_time"

    assert timeRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert timeRealUnit.convertTo(LammpsUnitSystem.METAL) == pytest.approx(0.001)

    timeMetalUnit = TimeQuantity(1.0, "lmp_metal_time")
    assert timeMetalUnit.getMagnitude() == 1.0
    assert timeMetalUnit.getUnits() == "lmp_metal_time"

    assert timeMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert timeMetalUnit.convertTo(LammpsUnitSystem.REAL) == pytest.approx(1000.0) 

    with pytest.raises(ValueError):
        failedTime = TimeQuantity(1.0, "m")

def test_VelocityQuantityDeclarations():
    velocityQuantity = VelocityQuantity(1.0, "m/s")
    assert velocityQuantity.getMagnitude() == 1.0
    assert velocityQuantity.getUnits() == "m/s"

    dict_result = velocityQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "m/s"
    assert dict_result["class"] == "VelocityQuantity"

    loadBackQuantity = VelocityQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "m/s"

    velocityRealUnit = VelocityQuantity(1.0, "lmp_real_velocity")
    assert velocityRealUnit.getMagnitude() == 1.0
    assert velocityRealUnit.getUnits() == "lmp_real_velocity"

    assert velocityRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert velocityRealUnit.convertTo(LammpsUnitSystem.METAL) == pytest.approx(1000.0)

    velocityMetalUnit = VelocityQuantity(1.0, "lmp_metal_velocity")
    assert velocityMetalUnit.getMagnitude() == 1.0
    assert velocityMetalUnit.getUnits() == "lmp_metal_velocity"

    assert velocityMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert velocityMetalUnit.convertTo(LammpsUnitSystem.REAL) == pytest.approx(0.001, 1e-3)

    with pytest.raises(ValueError):
        failedVelocity = VelocityQuantity(1.0, "m")

def test_EnergyQuantityDeclarations():
    energyQuantity = EnergyQuantity(1.0, "kcal/mol")
    assert energyQuantity.getMagnitude() == 1.0
    assert energyQuantity.getUnits() == "kcal/mol"

    dict_result = energyQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "kcal/mol"
    assert dict_result["class"] == "EnergyQuantity"

    loadBackQuantity = EnergyQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "kcal/mol"

    energyRealUnit = EnergyQuantity(1.0, "lmp_real_energy")
    assert energyRealUnit.getMagnitude() == 1.0
    assert energyRealUnit.getUnits() == "lmp_real_energy"

    # Conversion table: http://wild.life.nctu.edu.tw/class/common/energy-unit-conv-table-detail.html
    assert energyRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert energyRealUnit.convertTo(LammpsUnitSystem.METAL) == pytest.approx(0.0433634, 1e-3)

    energyMetalUnit = EnergyQuantity(1.0, "lmp_metal_energy")
    assert energyMetalUnit.getMagnitude() == 1.0
    assert energyMetalUnit.getUnits() == "lmp_metal_energy"

    assert energyMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert energyMetalUnit.convertTo(LammpsUnitSystem.REAL) == pytest.approx(23.0609, 1e-3)

    with pytest.raises(ValueError):
        failedEnergy = EnergyQuantity(1.0, "m")

def test_TemperatureQuantityDeclarations():
    temperatureQuantity = TemperatureQuantity(1.0, "K")
    assert temperatureQuantity.getMagnitude() == 1.0
    assert temperatureQuantity.getUnits() == "K"

    dict_result = temperatureQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "K"
    assert dict_result["class"] == "TemperatureQuantity"

    loadBackQuantity = TemperatureQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "K"

    temperatureRealUnit = TemperatureQuantity(1.0, "lmp_real_temperature")
    assert temperatureRealUnit.getMagnitude() == 1.0
    assert temperatureRealUnit.getUnits() == "lmp_real_temperature"

    assert temperatureRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert temperatureRealUnit.convertTo(LammpsUnitSystem.METAL) == pytest.approx(1.0, 1e-3)

    temperatureMetalUnit = TemperatureQuantity(1.0, "lmp_metal_temperature")
    assert temperatureMetalUnit.getMagnitude() == 1.0
    assert temperatureMetalUnit.getUnits() == "lmp_metal_temperature"

    assert temperatureMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert temperatureMetalUnit.convertTo(LammpsUnitSystem.REAL) == pytest.approx(1.0, 1e-3)

    with pytest.raises(ValueError):
        failedTemperature = TemperatureQuantity(1.0, "m")

def test_ForceQuantityDeclarations():
    forceQuantity = ForceQuantity(1.0, "kcal/mol/angstrom")
    assert forceQuantity.getMagnitude() == 1.0
    assert forceQuantity.getUnits() == "kcal/mol/angstrom"

    dict_result = forceQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "kcal/mol/angstrom"
    assert dict_result["class"] == "ForceQuantity"

    loadBackQuantity = ForceQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "kcal/mol/angstrom"

    forceRealUnit = ForceQuantity(1.0, "lmp_real_force")
    assert forceRealUnit.getMagnitude() == 1.0
    assert forceRealUnit.getUnits() == "lmp_real_force"

    assert forceRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert forceRealUnit.convertTo(LammpsUnitSystem.METAL) == pytest.approx(0.0433634, 1e-3)

    forceMetalUnit = ForceQuantity(1.0, "lmp_metal_force")
    assert forceMetalUnit.getMagnitude() == 1.0
    assert forceMetalUnit.getUnits() == "lmp_metal_force"

    assert forceMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert forceMetalUnit.convertTo(LammpsUnitSystem.REAL) == pytest.approx(23.0609, 1e-3)

    with pytest.raises(ValueError):
        failedForce = ForceQuantity(1.0, "m")

def test_TorqueQuantityDeclarations():
    torqueQuantity = TorqueQuantity(1.0, "kcal/mol")
    assert torqueQuantity.getMagnitude() == 1.0
    assert torqueQuantity.getUnits() == "kcal/mol"

    dict_result = torqueQuantity.to_dict()
    assert dict_result["magnitude"] == 1.0
    assert dict_result["units"] == "kcal/mol"
    assert dict_result["class"] == "TorqueQuantity"

    loadBackQuantity = TorqueQuantity()
    loadBackQuantity.from_dict(dict_result, version=0)

    assert loadBackQuantity.getMagnitude() == 1.0
    assert loadBackQuantity.getUnits() == "kcal/mol"

    torqueRealUnit = TorqueQuantity(1.0, "lmp_real_torque")
    assert torqueRealUnit.getMagnitude() == 1.0
    assert torqueRealUnit.getUnits() == "lmp_real_torque"

    assert torqueRealUnit.convertTo(LammpsUnitSystem.REAL) == 1.0
    assert torqueRealUnit.convertTo(LammpsUnitSystem.METAL) == pytest.approx(0.0433634, 1e-3)

    torqueMetalUnit = TorqueQuantity(1.0, "lmp_metal_torque")
    assert torqueMetalUnit.getMagnitude() == 1.0
    assert torqueMetalUnit.getUnits() == "lmp_metal_torque"

    assert torqueMetalUnit.convertTo(LammpsUnitSystem.METAL) == 1.0
    assert torqueMetalUnit.convertTo(LammpsUnitSystem.REAL) == pytest.approx(23.0609, 1e-3)

    with pytest.raises(ValueError):
        failedTorque = TorqueQuantity(1.0, "m")

    

if __name__ == "__main__":
    test_LengthQuantityDeclarations()

