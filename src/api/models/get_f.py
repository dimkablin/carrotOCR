"""Get files or folders function models."""
from typing import List
from pydantic import BaseModel


class GetFRequest(BaseModel):
    """Get files or folders function request."""
    count: int = -1
    path: str = "/"


class GetFilesResponse(BaseModel):
    """Get files or folders response."""
    files: List[str]


class GetFoldersResponse(BaseModel):
    """Get folders or folders response."""
    folders: List[str]
