import pytest 

from lammpsinputbuilder.quantities import *

def test_QuantityDeclarations():
    distanceQuantity = DistanceQuantity(1.0, "angstrom")
    assert distanceQuantity.getMagnitude() == 1.0
    assert distanceQuantity.getUnits() == "angstrom"

if __name__ == "__main__":
    test_QuantityDeclarations()

