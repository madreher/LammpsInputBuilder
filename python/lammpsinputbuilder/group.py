"""Module implementing the Group class and its subclasses."""

from typing import List
from enum import Enum


class Group:
    def __init__(self, group_name: str) -> None:
        self.group_name = group_name

    def get_group_name(self) -> str:
        return self.group_name

    def to_dict(self) -> dict:
        result = {}
        result["class"] = self.__class__.__name__
        result["group_name"] = self.group_name
        return result

    def from_dict(self, d: dict, version: int):
        self.group_name = d.get("group_name", "defaultGroupName")

    def add_do_commands(self) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class IndicesGroup(Group):
    def __init__(
            self,
            group_name: str = "defaultIndiceGroupName",
            indices: List[int] = []) -> None:
        super().__init__(group_name)
        self.indices = indices

        self.validateIndices()

    def validateIndices(self):
        # Check that all the indices are positive
        for index in self.indices:
            if index <= 0:
                raise ValueError(
                    f"Indices {index} declared in group {self.group_name}. Indices must be greater than 0 when creating an IndicesGroup.")

    def getIndices(self) -> List[int]:
        return self.indices

    def setIndices(self, indices: List[int]):
        self.indices = indices

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["indices"] = self.indices
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.indices = d.get("indices", [])
        self.validateIndices()

    def add_do_commands(self) -> str:
        if len(self.indices) == 0:
            return f"group {self.group_name} empty\n"
        else:
            commands = f"group {self.group_name} id"
            for index in self.indices:
                commands += f" {index}"
            commands += "\n"
            return commands

    def add_undo_commands(self) -> str:
        return f"group {self.group_name} delete\n"


class AllGroup(Group):
    def __init__(self) -> None:
        super().__init__("all")

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)

    def add_do_commands(self) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class EmptyGroup(Group):
    def __init__(self) -> None:
        super().__init__("empty")

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)

    def add_do_commands(self) -> str:
        return ""

    def add_undo_commands(self) -> str:
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

    def __init__(
            self,
            group_name: str = "defaultOperationGroupName",
            op: OperationGroupEnum = OperationGroupEnum.UNION,
            otherGroups: List[Group] = [
            EmptyGroup()]) -> None:
        super().__init__(group_name)
        self.op = op
        self.otherGroups = [g.get_group_name() for g in otherGroups]

        self.validateConfiguration()

    def validateConfiguration(self):
        if len(self.otherGroups) == 0 and self.op == OperationGroupEnum.UNION:
            raise ValueError(
                f"Union operation cannot be performed with an empty list of other groups when creating an {__class__.__name__}.")
        if len(
                self.otherGroups) < 2 and self.op in [
                OperationGroupEnum.SUBTRACT,
                OperationGroupEnum.INTERSECT]:
            raise ValueError(
                f"Operation {self.op} requires at least 2 other groups when creating an {__class__.__name__}.")

    def getOperation(self) -> OperationGroupEnum:
        return self.op

    def setOperation(self, op: OperationGroupEnum):
        self.op = op

    def getOtherGroups(self) -> List[str]:
        return self.otherGroups

    def setOtherGroups(self, otherGroups: List[Group]):
        self.otherGroups = [g.get_group_name() for g in otherGroups]

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["op"] = self.op.value
        result["otherGroups"] = self.otherGroups
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.otherGroups = d.get("otherGroups", [])

        self.validateConfiguration()

    def add_do_commands(self) -> str:
        self.validateConfiguration()
        commands = f"group {self.group_name} {OperationGroup.operationToStr[self.op]}"
        for grp in self.otherGroups:
            commands += f" {grp}"
        commands += "\n"
        return commands

    def add_undo_commands(self) -> str:
        return f"group {self.group_name} delete\n"


class ReferenceGroup(Group):
    def __init__(self, group_name: str = "defaultReferenceGroup",
                 reference: Group = AllGroup()) -> None:
        super().__init__(group_name)
        self.reference = reference.get_group_name()

    def get_group_name(self) -> str:
        return self.reference

    def getReferenceName(self) -> str:
        return self.reference

    def setReference(self, reference: Group):
        self.reference = reference.get_group_name()

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["reference"] = self.reference
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.reference = d.get("reference", "all")

    def add_do_commands(self) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class ManualGroup(Group):
    def __init__(
            self,
            group_name: str = "defaultManualGroup",
            do_cmd: str = "",
            undo_cmd: str = "") -> None:
        super().__init__(group_name)
        self.do_cmd = do_cmd
        self.undo_cmd = undo_cmd

    def get_do_cmd(self) -> str:
        return self.do_cmd

    def set_do_cmd(self, do_cmd: str):
        self.do_cmd = do_cmd

    def get_undo_cmd(self) -> str:
        return self.undo_cmd

    def set_undo_cmd(self, undo_cmd: str):
        self.undo_cmd = undo_cmd

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().from_dict(d, version=version)
        self.do_cmd = d.get("do_cmd", "")
        self.undo_cmd = d.get("undo_cmd", "")

    def add_do_commands(self) -> str:
        if self.do_cmd.endswith("\n"):
            return self.do_cmd

        return self.do_cmd + "\n"

    def add_undo_commands(self) -> str:
        if self.undo_cmd.endswith("\n"):
            return self.undo_cmd

        return self.undo_cmd + "\n"
