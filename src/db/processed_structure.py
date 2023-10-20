# pylint: disable=R0902
"""Structure of processed table."""
import json
from typing import List, Optional


class ProcessedStructure:
    """Data structure for each row for 'Processed' table."""
    uid: int = None
    directory: str = None
    old_filename: str = None
    new_filename: str = None
    tags: List[str] = None
    text: List[str] = None
    bboxes: List[List[int]] = None

    def __init__(self, **kwargs):
        if "directory" in kwargs:
            self.directory = kwargs.get("directory")
        if "old_filename" in kwargs:
            self.old_filename = kwargs.get("old_filename")
        if "new_filename" in kwargs:
            self.new_filename = kwargs.get("new_filename")
        if "tags" in kwargs:
            self.tags = kwargs.get("tags")
        if "text" in kwargs:
            self.text = kwargs.get("text")
        if "bboxes" in kwargs:
            self.bboxes = kwargs.get("bboxes")

    def from_db(self, raw: Optional[tuple]):
        """Convert data from db to template"""
        if not len(raw) == 0:
            self.uid = raw[0]
            self.directory = raw[1]
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
