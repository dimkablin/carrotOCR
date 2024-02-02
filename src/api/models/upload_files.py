"""Upload files function ai_models."""
from typing import List
from pydantic import BaseModel


class UploadFilesResponse(BaseModel):
    """Upload files function response."""
    paths: List[str]
