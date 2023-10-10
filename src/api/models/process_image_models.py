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
    file_path: str
    tags: List[str]
    text: List[str]
    bboxes: List[List[int]]


class ProcessImageResponse(BaseModel):
    """ Response of the OCR model """
    chunk_id: int  # Chunk ID
    results: List[Result]