# pylint: disable=R,E
"""Upload files function ai_models."""
from pydantic import BaseModel

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
