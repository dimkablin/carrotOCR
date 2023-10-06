"""Pipeline result model."""
from typing import List
from pydantic import BaseModel


class Result(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    file_path: str
    tags: List[str]
    text: List[str]
    bboxes: List[List[int]]
