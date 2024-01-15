"""Process chunk models."""
from typing import List
from pydantic import BaseModel

from src.api.models.process_image import ProcessImageResponse


class ProcessChunkRequest(BaseModel):
    """ Request to the OCR model """
    chunk_id: int  # Chunk ID
    ocr_model_type: str  # Model type


class ProcessChunkResponse(BaseModel):
    """ Response of the OCR model """
    chunk_id: int  # Chunk ID
    results: List[ProcessImageResponse]
    action: str = "chunk"


class ProgressResponse(BaseModel):
    """Progress bar response"""
    iter: int
    length: int
    message: str
    action: str = "progress_bar"
