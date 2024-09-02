from __future__ import annotations

class Quantity:
    def __init__(self, value: float, unit: str) -> None:
        self.value = value
        self.unit = unit

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["value"] = self.value
        result["unit"] = self.unit
        return result
    
    def fromDict(self, d: dict, version: int) -> None:
        self.value = d["value"]
        self.unit = d["unit"]

    def convertTo(self, unit: str) -> Quantity:
        raise NotImplementedError(f"Method not implemented by class {__class__}")
    
class TimeQuantity(Quantity):

    def __init__(self, value: float, unit: str) -> None:
        super().__init__(value, unit)

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