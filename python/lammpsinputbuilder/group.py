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
        result["groupName"] = self.groupName
        return result
        

    def fromDict(self, d: dict, version: int):
        self.groupName = d.get("groupName", "defaultGroupName")

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    

class IndicesGroup(Group):
    def __init__(self, groupName: str = "defaultIndiceGroupName", indices: List[int] = []) -> None:
        super().__init__(groupName)
        self.indices = indices

        self.validateIndices()

        
    def validateIndices(self):
        # Check that all the indices are positive
        for index in self.indices:
            if index <= 0:
                raise ValueError(f"Indices {index} declared in group {self.groupName}. Indices must be greater than 0 when creating an IndicesGroup.")


    def getIndices(self) -> List[int]:
        return self.indices
    
    def setIndices(self, indices: List[int]):
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
        super().fromDict(d, version=version)
        self.indices = d.get("indices", [])
        self.validateIndices()

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
        super().fromDict(d, version=version)

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""

class EmptyGroup(Group):
    def __init__(self) -> None:
        super().__init__("empty")
    
    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    
class OperationGroupEnum(Enum):
    SUBTRACT = 0,
    UNION = 1,
    INTERSECT = 2


    
class OperationGroup(Group):

    operationToStr = {
        OperationGroupEnum.SUBTRACT: "subtract",
        OperationGroupEnum.UNION: "union",
        OperationGroupEnum.INTERSECT: "intersect"
    }
    
    def __init__(self, groupName: str = "defaultOperationGroupName", op: OperationGroupEnum = OperationGroupEnum.UNION, otherGroups: List[Group] = [EmptyGroup()]) -> None:
        super().__init__(groupName)
        self.op = op
        self.otherGroups = [g.getGroupName() for g in otherGroups]

        self.validateConfiguration()

    def validateConfiguration(self):
        if len(self.otherGroups) == 0 and self.op == OperationGroupEnum.UNION:
            raise ValueError(f"Union operation cannot be performed with an empty list of other groups when creating an {__class__.__name__}.")
        if len(self.otherGroups) < 2 and self.op in [OperationGroupEnum.SUBTRACT, OperationGroupEnum.INTERSECT]:
            raise ValueError(f"Operation {self.op} requires at least 2 other groups when creating an {__class__.__name__}.")

    def getOperation(self) -> OperationGroupEnum:
        return self.op
    
    def setOperation(self, op: OperationGroupEnum):
        self.op = op

    def getOtherGroups(self) -> List[str]:
        return self.otherGroups
    
    def setOtherGroups(self, otherGroups: List[Group]):
        self.otherGroups = [g.getGroupName() for g in otherGroups]

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["op"] = self.op.value
        result["otherGroups"] = self.otherGroups
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.otherGroups = d.get("otherGroups", [])

        self.validateConfiguration()

    def addDoCommands(self) -> str:
        self.validateConfiguration()
        commands = f"group {self.groupName} {OperationGroup.operationToStr[self.op]}"
        for grp in self.otherGroups:
            commands += f" {grp}"
        commands += "\n"
        return commands

    def addUndoCommands(self) -> str:
        return f"group {self.groupName} delete\n"
    
class ReferenceGroup(Group):
    def __init__(self, groupName: str = "defaultReferenceGroup", reference: Group = AllGroup()) -> None:
        super().__init__(groupName)
        self.reference = reference.getGroupName()

    def getGroupName(self) -> str:
        return self.reference

    def getReferenceName(self) -> str:
        return self.reference
    
    def setReference(self, reference: Group):
        self.reference = reference.getGroupName()

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["reference"] = self.reference
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.reference = d.get("reference", "all")

    def addDoCommands(self) -> str:
        return ""

    def addUndoCommands(self) -> str:
        return ""
    
class ManualGroup(Group):
    def __init__(self, groupName: str = "defaultManualGroup", doCmd:str = "", undoCmd:str = "") -> None:
        super().__init__(groupName)
        self.doCmd = doCmd
        self.undoCmd = undoCmd

    def getDoCmd(self) -> str:
        return self.doCmd
    
    def setDoCmd(self, doCmd: str):
        self.doCmd = doCmd

    def getUndoCmd(self) -> str:
        return self.undoCmd
    
    def setUndoCmd(self, undoCmd: str):
        self.undoCmd = undoCmd

    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["doCmd"] = self.doCmd
        result["undoCmd"] = self.undoCmd
        return result

    def fromDict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.doCmd = d.get("doCmd", "")
        self.undoCmd = d.get("undoCmd", "")

    def addDoCommands(self) -> str:
        if self.doCmd.endswith("\n"):
            return self.doCmd
        else:
            return self.doCmd + "\n"

    def addUndoCommands(self) -> str:
        if self.undoCmd.endswith("\n"):
            return self.undoCmd
        else:
            return self.undoCmd + "\n"

    
    
    