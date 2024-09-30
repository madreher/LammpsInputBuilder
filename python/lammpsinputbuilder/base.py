import re

class BaseObject:

    def __init__(self, id_name:str = "default_id") -> None:
        self.id_name = id_name

        self.validate_id()

    def validate_id(self):
        # Check that the name is alpha numeric and start with a letter
        if not re.match(r'^[A-Za-z]\w+$', self.id_name):
            raise ValueError("Object name " + self.id_name +
                            " is not alpha numeric or doesn't start with a non letter.")

    def get_id_name(self) -> str:
        return self.id_name

    def set_id_name(self, id_name: str) -> None:
        self.id_name = id_name

    def to_dict(self) -> dict:
        return {
            "id_name": self.id_name
        }

    def from_dict(self, d: dict, version: int) -> None:
        del version  # unused
        self.id_name = d["id_name"]

        self.validate_id()
