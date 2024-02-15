# pylint: disable=R,E
"""Get OCR Models FastAPI model."""
from typing import List
from pydantic import BaseModel


class GetOCRModelsResponse(BaseModel):
    """List of OCR Models structures."""
    models: List[str]
    default: int


class Cut(BaseModel):
    """Area to process"""
    x1: int
    y1: int
    width: int
    height: int


class PipelineParams(BaseModel):
    """Pipeline params"""
    angle: int  # Angle to rotate the image
    w2h_koeff: float  # Width to height koeff
    cut: Cut  # Area to process


class ProcessImageRequest(BaseModel):
    """ Request to the OCR model """
    uid: int  # Image ID
    ocr_model_type: str  # Model type
    pipeline_params: PipelineParams  # how to


class ProcessImageResponse(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    old_filename: str
    duplicate_id: int  # Duplicate ID if it is already in database
    filetype: str = 'image'


class ProcessFileResponse(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    old_filename: str
    duplicate_id: int  # Duplicate ID if it is already in database
    file_type: str = None
    heirs: List[ProcessImageResponse] = None

    def process_image_response(self):
        """convert to ProcessImageResponse class"""
        return ProcessImageResponse(
            uid=self.uid,
            old_filename=self.old_filename,
            duplicate_id=self.duplicate_id,
            filetype='file'
        )


class ProcessChunkRequest(BaseModel):
    """ Request to the OCR model """
    chunk_id: int  # Chunk ID
    ocr_model_type: str  # Model type


class ProcessChunkResponse(BaseModel):
    """ Response of the OCR model """
    chunk_id: int  # Chunk ID
    results: List[ProcessFileResponse]
    action: str = "chunk"


class ProgressResponse(BaseModel):
    """Progress bar response"""
    iter: int
    length: int
    message: str
    action: str = "progress_bar"
