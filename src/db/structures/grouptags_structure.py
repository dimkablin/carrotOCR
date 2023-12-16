# pylint: disable=R
"""Structure of grouptags table."""
from typing import Optional

class GrouptagsStructure:
    """Data structure for each row for 'permatags' table."""
    uid: int = None
    name: str = None

    def __init__(self, **kwargs):
        for attr_name in dir(self):
            if not attr_name.startswith("__") and attr_name in kwargs:
                setattr(self, attr_name, kwargs[attr_name])

    def from_db(self, raw: Optional[tuple]):
        """Convert data from db to template"""
        if not len(raw) == 0:
            self.uid = raw[0]
            self.name = raw[1]
            return self
        return None

    def to_db(self) -> dict:
        """Convert self members to dict avoiding None."""
        result = {}
        for attr, value in self.__dict__.items():
            if value is not None:
                result[attr] = value

        return result

    def __str__(self):
        result = ""
        for attr, value in self.__dict__.items():
            result += f"{attr}: " + str(value) + "\n"
        return result
