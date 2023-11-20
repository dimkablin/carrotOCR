"""process image models."""
from pydantic import BaseModel


class Cut(BaseModel):
    """Area to process"""
    x1: int
    y1: int
    x2: int
    y2: int


class PipelineParams(BaseModel):
    """Pipeline params"""
    angle: int  # Angle to rotate the image
    w2h_koeff: float # Width to heigth koeff
    cut: Cut # Area to process


class ProcessImageRequest(BaseModel):
    """ Request to the OCR model """
    uid: int  # Image ID
    ocr_model_type: str # Model type
    pipeline_params: PipelineParams # how to


class ProcessImageResponse(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    old_filename: str
    duplicate_id: int  # Duplicate ID if it is already in database
