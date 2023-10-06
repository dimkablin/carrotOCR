"""Pipeline response model."""
from typing import List
from pydantic import BaseModel
from src.api.models.result import Result


class OCRResponse(BaseModel):
    """ Response of the OCR model """
    chunk_id: int  # Chunk ID
    results: List[Result]
