"""Add filenames function models"""

from typing import List
from pydantic import BaseModel


class AddFilenameRequest(BaseModel):
    """Add filename function request"""
    uid: int
    filename: str
    is_duplicate: bool


class AddFilenamesRequest(BaseModel):
    """Add filenames function request"""
    reqs: List[AddFilenameRequest]
