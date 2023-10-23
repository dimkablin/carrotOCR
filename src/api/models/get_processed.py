"""get_processed function models."""
from typing import List, Optional

from pydantic import BaseModel


class GetProcessedRequest(BaseModel):
    """get_processed function request"""
    uid: int


class GetProcessedResponse(BaseModel):
    """get_processed function response"""
    path: str
    old_filename: str
    new_filename: Optional[str]
    tags: Optional[List[str]]
    text: List[str]
    bboxes: List[List[int]]
