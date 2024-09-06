import pytest 

from lammpsinputbuilder.quantities import *

def test_LengthQuantityDeclarations():
    lengthQuantity = LengthQuantity(1.0, "angstrom")
    assert lengthQuantity.getMagnitude() == 1.0
    assert lengthQuantity.getUnits() == "angstrom"

    dictResult = lengthQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "angstrom"
    assert dictResult["class"] == "LengthQuantity"

    loadBackQuantity = LengthQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

    dictResult = timeQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "ps"
    assert dictResult["class"] == "TimeQuantity"

    loadBackQuantity = TimeQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

    dictResult = velocityQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "m/s"
    assert dictResult["class"] == "VelocityQuantity"

    loadBackQuantity = VelocityQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

    dictResult = energyQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "kcal/mol"
    assert dictResult["class"] == "EnergyQuantity"

    loadBackQuantity = EnergyQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

    dictResult = temperatureQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "K"
    assert dictResult["class"] == "TemperatureQuantity"

    loadBackQuantity = TemperatureQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

    dictResult = forceQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "kcal/mol/angstrom"
    assert dictResult["class"] == "ForceQuantity"

    loadBackQuantity = ForceQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

    dictResult = torqueQuantity.toDict()
    assert dictResult["magnitude"] == 1.0
    assert dictResult["units"] == "kcal/mol"
    assert dictResult["class"] == "TorqueQuantity"

    loadBackQuantity = TorqueQuantity()
    loadBackQuantity.fromDict(dictResult, version=0)

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

