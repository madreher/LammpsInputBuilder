"""Module implementing the Group class and its subclasses."""

from typing import List
from enum import IntEnum
from lammpsinputbuilder.base import BaseObject


class Group(BaseObject):
    def __init__(self, group_name: str = "defaultGroupName") -> None:
        super().__init__(id_name=group_name)

    def get_group_name(self) -> str:
        return super().get_id_name()

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__

        return result

    def add_do_commands(self) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class IndicesGroup(Group):
    def __init__(
            self,
            group_name: str = "defaultIndiceGroupName",
            indices: List[int] = None) -> None:
        super().__init__(group_name)

        if indices is None:
            self.indices = []
        else:
            self.indices = indices

        self.validate_indices()

    def validate_indices(self):
        # Check that all the indices are positive
        for index in self.indices:
            if index <= 0:
                raise ValueError(
                    (f"Indices {index} declared in group {self.group_name}. "
                     "Indices must be greater than 0 when creating an IndicesGroup."))

    def get_indices(self) -> List[int]:
        return self.indices

    def set_indices(self, indices: List[int]):
        self.indices = indices

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["indices"] = self.indices
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.indices = d.get("indices", [])
        self.validate_indices()

    def add_do_commands(self) -> str:
        if len(self.indices) == 0:
            return f"group {self.get_group_name()} empty\n"

        commands = f"group {self.get_group_name()} id"
        for index in self.indices:
            commands += f" {index}"
        commands += "\n"
        return commands

    def add_undo_commands(self) -> str:
        return f"group {self.get_group_name()} delete\n"


class AllGroup(Group):
    def __init__(self) -> None:
        super().__init__("all")

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
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
        result["class_name"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)

    def add_do_commands(self) -> str:
        return ""

    def add_undo_commands(self) -> str:
        return ""


class OperationGroupEnum(IntEnum):
    SUBTRACT = 0
    UNION = 1
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
            other_groups: List[Group] = None) -> None:
        super().__init__(group_name)
        self.op = op
        if other_groups is None:
            self.other_groups = [EmptyGroup().get_group_name()]
        else:
            self.other_groups = [g.get_group_name() for g in other_groups]

        self.validate_configuration()

    def validate_configuration(self):
        if len(self.other_groups) == 0 and self.op == OperationGroupEnum.UNION:
            raise ValueError(
                ("Union operation cannot be performed with an empty list of "
                 f"other groups when creating an {__class__.__name__}."))
        if len(
                self.other_groups) < 2 and self.op in [
                OperationGroupEnum.SUBTRACT,
                OperationGroupEnum.INTERSECT]:
            raise ValueError(
                (f"Operation {self.op} requires at least 2 other groups "
                 f"when creating an {__class__.__name__}."))

    def get_operation(self) -> OperationGroupEnum:
        return self.op

    def set_operation(self, op: OperationGroupEnum):
        self.op = op

    def get_other_groups(self) -> List[str]:
        return self.other_groups

    def set_other_groups(self, other_groups: List[Group]):
        self.other_groups = [g.get_group_name() for g in other_groups]

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["op"] = self.op.value
        result["other_groups_name"] = self.other_groups
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.other_groups = d.get("other_groups_name", [])

        self.validate_configuration()

    def add_do_commands(self) -> str:
        self.validate_configuration()
        commands = f"group {self.get_group_name()} {OperationGroup.operationToStr[self.op]}"
        for grp in self.other_groups:
            commands += f" {grp}"
        commands += "\n"
        return commands

    def add_undo_commands(self) -> str:
        return f"group {self.get_group_name()} delete\n"


class ReferenceGroup(Group):
    def __init__(self, group_name: str = "defaultReferenceGroup",
                 reference: Group = AllGroup()) -> None:
        super().__init__(group_name)
        self.reference = reference.get_group_name()

    def get_group_name(self) -> str:
        return self.reference

    def get_reference_name(self) -> str:
        return self.reference

    def set_reference(self, reference: Group):
        self.reference = reference.get_group_name()

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["reference_name"] = self.reference
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.reference = d.get("reference_name", "all")

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
        result["class_name"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        return result

    def from_dict(self, d: dict, version: int):
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
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
