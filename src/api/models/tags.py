# pylint: disable=R,E
"""Upload files function models."""
from pydantic import BaseModel

class GetTagsResponse(BaseModel):
    """Get Tags function response."""
    tags: list[str]

class RemoveTagsResponse(BaseModel):
    """Remove Tags function response."""
    response: bool
