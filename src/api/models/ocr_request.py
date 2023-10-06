"""Pipeline request."""
from typing import List
from pydantic import BaseModel


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    chunk_id: int  # Chunk ID
    paths: List[str]
