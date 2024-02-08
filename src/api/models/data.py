"""Request and Response FastAPI Models"""

from typing import List
from pydantic import BaseModel

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp"}
FILE_EXTENSIONS = {"pdf", "xps", "epub", "mobi", "fb2", "cbz", "txt"}


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


class UploadFilesResponse(BaseModel):
    """Upload files function response."""
    paths: List[str]
