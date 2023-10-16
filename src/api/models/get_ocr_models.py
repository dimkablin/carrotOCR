"""Get OCR Models FastAPI model."""
from typing import List
from pydantic import BaseModel


class GetOCRModelsResponse(BaseModel):
    """List of OCR Models structures."""
    models: List[str]
