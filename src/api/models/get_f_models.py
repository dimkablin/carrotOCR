"""Get files or folders function models."""
from typing import List
from pydantic import BaseModel


class GetFRequest(BaseModel):
    """Get files or folders function request."""
    count: int = -1
    path: str = "/"


class GetFResponse(BaseModel):
    """Get files or folders response."""
    paths: List[str]
