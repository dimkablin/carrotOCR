# pylint: disable=R0902
"""Structure of processed table."""
import json
from typing import List, Optional


class ProcessedStructure:
    """Data structure for each row for 'Processed' table."""
    uid: int = None
    chunk_id: int = None
    old_filename: str = None
    new_filename: str = None
    tags: List[str] = None
    text: List[str] = None
    bboxes: List[List[int]] = None

    def __init__(self, **kwargs):
        for attr_name in dir(self):
            if not attr_name.startswith("__") and attr_name in kwargs:
                setattr(self, attr_name, kwargs[attr_name])

    def from_db(self, raw: Optional[tuple]):
        """Convert data from db to template"""
        if not len(raw) == 0:
            self.uid = raw[0]
            self.chunk_id = raw[1]
            self.old_filename = raw[2]
            self.new_filename = raw[3]
            self.tags = raw[4]
            self.text = raw[5]
            self.bboxes = json.loads(raw[6])
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
