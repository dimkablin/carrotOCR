"""get_processed function models."""
from typing import List

from pydantic import BaseModel


class GetProcessedRequest(BaseModel):
    uid: int


class GetProcessedResponse(BaseModel):
    path: str
    old_filename: str
    new_filename: str
    tags: List[str]
    text: List[str]
    bboxes: List[List[int]]
