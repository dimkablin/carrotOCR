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
    angle: int
    old_filename: str
    new_filename: Optional[str]
    tags: Optional[List[str]]
    text: List[str]
    bboxes: List[TBox]


class PermatagsResponse(BaseModel):
    """Data structure for each row for 'permatags' table."""
    uid: int
    tag: str
    group_id: int


class GetPermatagsResponse(BaseModel):
    """List of permatags"""
    tags: list[PermatagsResponse]


class RemoveTagsResponse(BaseModel):
    """Remove Tags function response."""
    response: bool


class GrouptagsResponse(BaseModel):
    """Get names of group of tags"""
    uid: int
    name: str


class AddFilenameRequest(BaseModel):
    """Add filename function request"""
    uid: int
    filename: str
    is_duplicate: bool = False


class AddFilenamesRequest(BaseModel):
    """Add filenames function request"""
    reqs: List[AddFilenameRequest]
