"""Process image models."""
from typing import List
from pydantic import BaseModel


class ProcessImageRequest(BaseModel):
    """ Request to the OCR model """
    chunk_id: int  # Chunk ID
    paths: List[str]


class Result(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    duplicate_id: int  # Duplicate ID if it is already in database


class ProcessImageResponse(BaseModel):
    """ Response of the OCR model """
    chunk_id: int  # Chunk ID
    results: List[Result]
