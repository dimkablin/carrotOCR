"""process image models."""
from pydantic import BaseModel


class ProcessImageRequest(BaseModel):
    """ Request to the OCR model """
    uid: int  # Image ID
    model_type: str # Model type
    angle_to_rotate: int  # Angle to rotate the image


class ProcessImageResponse(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    old_filename: str
    duplicate_id: int  # Duplicate ID if it is already in database
