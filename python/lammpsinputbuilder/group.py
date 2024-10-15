"""Module implementing the Group class and its subclasses."""

from typing import List
from enum import IntEnum
from lammpsinputbuilder.base import BaseObject


class Group(BaseObject):
    """
    Base class for all groups. A Group represents a list of selected 
    atoms. Each subclass represents a different method to select atoms.

    A Group object has a scope, and therfor must provide a way to declare the 
    computations, but also how to un-declare them. This is done by overriding
    the `add_do_commands()` and `add_undo_commands()` methods. Each subclass 
    implementing a new Group must implement both these methods.

    This class should never be instantiated directly. Instead, the subclasses
    should implement the `add_do_commands()` and `add_undo_commands()` methods.

    Lammps documentation: https://docs.lammps.org/group.html
    """
    def __init__(self, group_name: str = "defaultGroupName") -> None:
        """
        Constructor
        Args:
            group_name (str): The name of the group. The name must be alpha numeric
                            and start with a letter

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        super().__init__(id_name=group_name)

    def get_group_name(self) -> str:
        """
        Get the name of the group

        Returns:
            str: The name of the group
        """
        return super().get_id_name()

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the group.

        Returns:
            dict: The dictionary representation of the group.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__

        return result

    def add_do_commands(self) -> str:
        """
        Generate the commands to declare the group

        Returns:
            str: Lammps command(s)

        Raises:
            NotImplementedError: If the method is not implemented by the subclass
        """
        raise NotImplementedError((f"Method not implemented by class {__class__}. This method"
                                   " must be overridden by any subclasses of Group"))

    def add_undo_commands(self) -> str:
        """
        Generate the commands to un-declare the group

        Returns:
            str: Lammps command(s)

        Raises:
            NotImplementedError: If the method is not implemented by the subclass
        """
        raise NotImplementedError((f"Method not implemented by class {__class__}. This method"
                                   " must be overridden by any subclasses of Group"))


class IndicesGroup(Group):
    """
    Select a list of atoms by their atom indices. Indices start at 1.
    Lammps documentation: https://docs.lammps.org/group.html
    """
    def __init__(
            self,
            group_name: str = "defaultIndiceGroupName",
            indices: List[int] = None) -> None:
        """
        Constructor
        Args:
            group_name (str): The name of the group. The name must be alpha numeric
                            and start with a letter
            indices (List[int]): The indices of the atoms

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If an indices is inferior to 1
        """
        super().__init__(group_name)

        if indices is None:
            self.indices = []
        else:
            self.indices = indices

        self.validate_indices()

    def validate_indices(self):
        """
        Check that all the indices are positive.

        Returns:
            None

        Raise:
            ValueError: If an indices is inferior to 1
        """
        # Check that all the indices are positive
        for index in self.indices:
            if index <= 0:
                raise ValueError(
                    (f"Indices {index} declared in group {self.group_name}. "
                     "Indices must be greater than 0 when creating an IndicesGroup."))

    def get_indices(self) -> List[int]:
        """
        Get the list of indices

        Returns:
            List[int]: The list of indices
        """
        return self.indices

    def set_indices(self, indices: List[int]):
        """
        Set the list of indices

        Args:
            indices (List[int]): The list of indices

        Returns:
            None

        Raise:
            ValueError: If an indices is inferior to 1
        """
        self.indices = indices
        self.validate_indices()

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the group.

        Returns:
            dict: The dictionary representation of the group.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["indices"] = self.indices
        return result

    def from_dict(self, d: dict, version: int):
        """
        Read the dictionary representation of the group.

        Args:
            d (dict): The dictionary representation of the group.
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or doesn't match the class name
        """
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.indices = d.get("indices", [])
        self.validate_indices()

    def add_do_commands(self) -> str:
        """
        Generate the commands to declare the group

        Returns:
            str: Lammps command(s)
        """
        if len(self.indices) == 0:
            return f"group {self.get_group_name()} empty\n"

        commands = f"group {self.get_group_name()} id"
        for index in self.indices:
            commands += f" {index}"
        commands += "\n"
        return commands

    def add_undo_commands(self) -> str:
        """
        Generate the commands to un-declare the group

        Returns:
            str: Lammps command(s)
        """
        return f"group {self.get_group_name()} delete\n"


class AllGroup(Group):
    """
    Group class to represent the default group "all". This group is created 
    by Lammps by default, and doesn't require to be declared, removed, 
    and doesn't have a scope.

    Lammps documentation: https://docs.lammps.org/group.html
    """
    def __init__(self) -> None:
        """
        Constructor

        Returns:
            None
        """
        super().__init__("all")

    def to_dict(self) -> dict:
        """"
        Generate a dictionary representation of the group.

        Returns:
            dict: The dictionary representation of the group.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        """
        Read the dictionary representation of the group.

        Args:
            d (dict): The dictionary representation of the group.
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or doesn't match the class name
        """
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)

    def add_do_commands(self) -> str:
        """
        Get the Lammps commands to declare the group

        Returns:
            str: Lammps command(s)
        """
        return ""

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to un-declare the group

        Returns:
            str: Lammps command(s)
        """
        return ""


class EmptyGroup(Group):
    """
    Group class to represent the default group "empty". This group is created 
    by default, and doesn't require to be declared, removed, and doesn't have a scope.

    Lammps documentation: https://docs.lammps.org/group.html
    """
    def __init__(self) -> None:
        """
        Constructor

        Returns:
            None
        """
        super().__init__("empty")

    def to_dict(self) -> dict:
        """
        Generate a dictionary representation of the group.

        Returns:
            dict: The dictionary representation of the group.
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        return result

    def from_dict(self, d: dict, version: int):
        """
        Read the dictionary representation of the group.

        Args:
            d (dict): The dictionary representation of the group.
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or doesn't match the class name
        """
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)

    def add_do_commands(self) -> str:
        """
        Get the Lammps commands to declare the group

        Returns:
            str: Lammps command(s)
        """
        return ""

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to un-declare the group

        Returns:
            str: Lammps command(s)
        """
        return ""


class OperationGroupEnum(IntEnum):
    SUBTRACT = 0
    UNION = 1
    INTERSECT = 2


class OperationGroup(Group):
    """
    Group class to represent groups creating by applying an operation between 
    other groups. This class currently only support subtract, union, and intersect 
    operations. If you need other operations, please use the ManualGroup class instead.

    Lammps documentation: https://docs.lammps.org/group.html
    """

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
        """
        Constructor
        Args:
            group_name (str): The name of the group. The name must be alpha numeric
                            and start with a letter
            op (OperationGroupEnum): The operation to perform
            other_groups (List[Group]): The other groups

        Returns:
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
            ValueError: If not enough groups are provided for the operation
        """
        super().__init__(group_name)
        self.op = op
        if other_groups is None:
            self.other_groups = [EmptyGroup().get_group_name()]
        else:
            self.other_groups = [g.get_group_name() for g in other_groups]

        self.validate_configuration()

    def validate_configuration(self):
        """
        Validate the configuration of the operation group

        Returns:
            None

        Raise:
            ValueError: If no groups are provided for the operation UNION
            ValueError: If 1 or less groups are provided for the operation SUBSTRACT or INTERSECT
        """

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
        """
        Get the operation

        Returns:
            OperationGroupEnum: The operation
        """
        return self.op

    def set_operation(self, op: OperationGroupEnum):
        """
        Set the operation

        Args:
            op (OperationGroupEnum): The operation

        Returns:
            None

        Raise:
            ValueError: If not enough groups are provided for the operation
        """
        self.op = op
        self.validate_configuration()

    def get_other_groups(self) -> List[str]:
        """
        Get the other groups

        Returns:
            List[str]: The other groups
        """
        return self.other_groups

    def set_other_groups(self, other_groups: List[Group]):
        """
        Set the other groups

        Args:
            other_groups (List[Group]): The other groups

        Returns:
            None

        Raise:
            ValueError: If not enough groups are provided for the operation
        """
        self.other_groups = [g.get_group_name() for g in other_groups]
        self.validate_configuration()

    def to_dict(self) -> dict:
        """
        Get the dictionary representation of the object

        Returns:
            dict: The dictionary representation
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["op"] = self.op.value
        result["other_groups_name"] = self.other_groups
        return result

    def from_dict(self, d: dict, version: int):
        """
        Read the dictionary representation of the group.

        Args:
            d (dict): The dictionary representation of the group.
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or doesn't match the class name
        """
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.other_groups = d.get("other_groups_name", [])

        self.validate_configuration()

    def add_do_commands(self) -> str:
        """
        Get the Lammps commands to declare the group.

        Returns:
            str: Lammps command(s)
        """
        self.validate_configuration()
        commands = f"group {self.get_group_name()} {OperationGroup.operationToStr[self.op]}"
        for grp in self.other_groups:
            commands += f" {grp}"
        commands += "\n"
        return commands

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to delete the group.

        Returns:
            str: Lammps command(s)
        """
        return f"group {self.get_group_name()} delete\n"


class ReferenceGroup(Group):
    """
    Group class to implement a reference to another group. A ReferenceGroup is a non owning  
    group pointing to another group. This class should be used to point to another group 
    which is already defined within the current scope.
    """
    def __init__(self, group_name: str = "defaultReferenceGroup",
                 reference: Group = AllGroup()) -> None:
        """
        Initializes a new instance of the ReferenceGroup class.

        Parameters:
        group_name (str): The name of the group. Defaults to "defaultReferenceGroup".
        reference (Group): The reference group. Defaults to AllGroup.

        Returns:
        None
        """
        self.reference = reference
        super().__init__(group_name)
        self.reference = reference.get_group_name()

    def get_group_name(self) -> str:
        """
        Get the group name

        Returns:
            str: The group name
        """
        return self.reference

    def get_reference_name(self) -> str:
        """
        Get the reference name

        Returns:
            str: The reference name
        """
        return self.reference

    def set_reference(self, reference: Group):
        """
        Set the reference

        Args:
            reference (Group): The reference

        Returns:
            None
        """
        self.reference = reference.get_group_name()

    def to_dict(self) -> dict:
        """
        Get the dictionary representation of the object

        Returns:
            dict: The dictionary representation
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["reference_name"] = self.reference
        return result

    def from_dict(self, d: dict, version: int):
        """
        Read the dictionary representation of the group.

        Args:
            d (dict): The dictionary representation of the group.
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or doesn't match the class name
        """
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.reference = d.get("reference_name", "all")

    def add_do_commands(self) -> str:
        """
        Get the Lammps commands to declare the group. In this case,
        nothing to declare as the reference group must already be defined.

        Returns:
            str: Lammps command(s)
        """
        return ""

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to delete the group. In this case,
        nothing to do as the group deletion will be done by the reference.

        Returns:
            str: Lammps command(s)
        """
        return ""


class ManualGroup(Group):
    """
    A ManualGroup is a way for the user to define a group by manually writing commands.
    The user is responsible for providing the right commands to both create and delete
    the group.
    """
    def __init__(
            self,
            group_name: str = "defaultManualGroup",
            do_cmd: str = "",
            undo_cmd: str = "") -> None:
        """
        Constructor 

        Args:
            group_name (str): The name of the group. Defaults to "defaultManualGroup".
            do_cmd (str): The command to create the group. Defaults to "".
            undo_cmd (str): The command to delete the group. Defaults to "".

        Returns:
            None
        """
        super().__init__(group_name)
        self.do_cmd = do_cmd
        self.undo_cmd = undo_cmd

    def get_do_cmd(self) -> str:
        """
        Get the do command

        Returns:
            str: The do command
        """
        return self.do_cmd

    def set_do_cmd(self, do_cmd: str):
        """
        Set the do command

        Args:
            do_cmd (str): The do command

        Returns:
            None
        """
        self.do_cmd = do_cmd

    def get_undo_cmd(self) -> str:
        """
        Get the undo command

        Returns:
            str: The undo command
        """
        return self.undo_cmd

    def set_undo_cmd(self, undo_cmd: str):
        """
        Set the undo command

        Args:
            undo_cmd (str): The undo command

        Returns:
            None
        """
        self.undo_cmd = undo_cmd

    def to_dict(self) -> dict:
        """
        Get the dictionary representation of the object

        Returns:
            dict: The dictionary representation
        """
        result = super().to_dict()
        result["class_name"] = self.__class__.__name__
        result["do_cmd"] = self.do_cmd
        result["undo_cmd"] = self.undo_cmd
        return result

    def from_dict(self, d: dict, version: int):
        """
        Read the dictionary representation of the group.

        Args:
            d (dict): The dictionary representation of the group.
            version (int): The version of the dictionary representation

        Returns:
            None

        Raise:
            ValueError: If the class name is not found or doesn't match the class name
        """
        # Make sure that we are reading the right class
        if d["class_name"] != self.__class__.__name__:
            raise ValueError(
                f"Expected class {self.__class__.__name__}, got {d['class_name']}.")
        super().from_dict(d, version=version)
        self.do_cmd = d.get("do_cmd", "")
        self.undo_cmd = d.get("undo_cmd", "")

    def add_do_commands(self) -> str:
        """
        Get the Lammps commands to declare the group.

        Returns:
            str: Lammps command(s)
        """
        if self.do_cmd.endswith("\n"):
            return self.do_cmd

        return self.do_cmd + "\n"

    def add_undo_commands(self) -> str:
        """
        Get the Lammps commands to delete the group.

        Returns:
            str: Lammps command(s)
        """
        if self.undo_cmd.endswith("\n"):
            return self.undo_cmd

        return self.undo_cmd + "\n"
