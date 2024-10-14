import re

class BaseObject:
    """
    Base class for all the objects which do have a scope and must be 
    identifiable by an ID.

    Dev note: At some point, the workflow will have to check for the uniqueness of the ID
    within a scope. It is however still unclear where that check would be placed.
    """

    def __init__(self, id_name:str = "default_id") -> None:
        """
        Args:
            id_name (str): The name of the object. The name must be alpha numeric and start with a letter
        Returns:
            None
        """
        self.id_name = id_name

        self.validate_id()

    def validate_id(self):
        """
        Check that the name is alpha numeric and start with a letter

        Returns: 
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        # Check that the name is alpha numeric and start with a letter
        if not re.match(r'^[A-Za-z]\w+$', self.id_name):
            raise ValueError("Object name " + self.id_name +
                            " is not alpha numeric or doesn't start with a non letter.")

    def get_id_name(self) -> str:
        """
        Return the name of the object

        Returns: 
            str: The name of the object
        """
        return self.id_name

    def set_id_name(self, id_name: str) -> None:
        """
        Set the name of the object and validate it

        Args:
            id_name (str): The new name of the object

        Returns: 
            None

        Raise:
            ValueError: If the name is not alpha numeric or doesn't start with a non letter
        """
        self.id_name = id_name
        self.validate_id()

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary

        Returns: 
            dict: The object as a dictionary
        """
        return {
            "id_name": self.id_name
        }

    def from_dict(self, d: dict, version: int) -> None:
        """
        Parse the dictionary representation of the object and load it into 
        the current object.

        Args:
            d (dict): The dictionary representation of the object.
            version (int): The version of the dictionary representation.

        Returns:
            None

        Raise:
            ValueError: If the version is not supported.
        """
        if version != 0:
            raise ValueError(f"Unsupported version {version}")

        self.id_name = d["id_name"]

        self.validate_id()
