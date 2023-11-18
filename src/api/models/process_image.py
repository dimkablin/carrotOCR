"""process image models."""
from pydantic import BaseModel


class PipelineParams(BaseModel):
    """Pipeline params"""
    angle_to_rotate: int  # Angle to rotate the image
    w2h_koeff: float # Width to heigth koeff
    area_to_process: list[int] # [x1 y1 x2 y2]


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
