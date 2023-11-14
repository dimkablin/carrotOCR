"""Upload files function models."""
from typing import List
from pydantic import BaseModel


class GetTagsResponse(BaseModel):
    """Get Tags function response."""
    tags: List[str]

class RemoveTagsResponse(BaseModel):
    """Remove Tags function response."""
    response: bool