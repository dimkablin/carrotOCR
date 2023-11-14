"""get_processed function models."""
from typing import List, Optional
from pydantic import BaseModel

class TBox(BaseModel):
    """Part of GetProcessed Response represented bbox."""
    x: int
    y: int
    w: int
    h: int

class GetProcessedRequest(BaseModel):
    """get_processed function request"""
    uid: int

class GetProcessedResponse(BaseModel):
    """get_processed function response"""
    chunk_id: int
    old_filename: str
    new_filename: Optional[str]
    tags: Optional[List[str]]
    text: List[str]
    bboxes: List[TBox]
