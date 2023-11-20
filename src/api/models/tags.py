# pylint: disable=R,E
"""Upload files function models."""
from typing import Any
from pydantic import BaseModel

class GetTagsResponse(BaseModel):
    """Get Tags function response."""
    tags: list[dict[Any, Any]]

class RemoveTagsResponse(BaseModel):
    """Remove Tags function response."""
    response: bool
