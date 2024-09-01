from typing import List
from enum import Enum

class Group:
    def __init__(self, groupName: str) -> None:
        self.groupName = groupName

    def getGroupName(self) -> str:
        return self.groupName

    def toDict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["name"] = self.groupName
        return result
        

    def fromDict(self, d: dict, version: int):
        self.groupName = d["name"]

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    

class IndicesGroup(Group):
    def __init__(self, groupName: str, indices: List[int] = []) -> None:
        super().__init__(groupName)
        self.indices = indices

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["indices"] = self.indices
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d)
        self.indices = d["indices"]

    def addDoCommands(self) -> str:
        if len(self.indices) == 0:
            return f"group {self.groupName} empty\n"
        else:
            commands = f"group {self.groupName} id"
            for index in self.indices:
                commands += f" {index}"
            commands += "\n"
            return commands

    def addUndoCommands(self) -> str:
        return f"group {self.groupName} delete\n"
    
class OperationGroupEnum(Enum):
    SUBTRACT = 0,
    UNION = 1,
    INTERSECT = 2


class OperationGroup(Group):
    def __init__(self, groupName: str, op: OperationGroupEnum = OperationGroupEnum.UNION, otherGroups: List[str] = []) -> None:
        super().__init__(groupName)
        self.op = op
        self.otherGroups = otherGroups

        # We are not checking the validity of the setup here because some classes require to create this object with default values
        # and then initialize from a dict.

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["op"] = self.op.value
        result["otherGroups"] = [group.getGroupName() for group in self.otherGroups]
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d)
        self.otherGroups = d["otherGroups"]

        if len(self.otherGroups) == 0 and self.op == OperationGroupEnum.UNION:
            raise ValueError(f"Union operation cannot be performed with an empty list of other groups when creating an {__class__.__name__}.")
        if len(self.otherGroups) < 2 and self.op in [OperationGroupEnum.SUBTRACT, OperationGroupEnum.INTERSECT]:
            raise ValueError(f"Operation {self.op} requires at least 2 other groups when creating an {__class__.__name__}.")

    def addDoCommands(self) -> str:
        commands = f"group {self.groupName} id"
        for index in self.indices:
            commands += f" {index}"
        commands += "\n"
        return commands

    def addUndoCommands(self) -> str:
        return f"group {self.groupName} delete\n"
    
class AllGroup(Group):
    def __init__(self) -> None:
        super().__init__("all")
    
    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d)

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

    