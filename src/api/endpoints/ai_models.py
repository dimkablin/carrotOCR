"""ML model router"""

from fastapi import APIRouter

from src.ai_models.find_tags import FIND_TAGS_MODEL
from src.ai_models.ocr import OCR_MODEL
from src.api.crud.ai_models import AIModels
from src.api.models.ai_models import *

router = APIRouter()


@router.get("/get-ocr-models/", response_model=GetOCRModelsResponse)
def get_ocr_models():
    """Return OCR Models ids and its names."""
    return AIModels.get_ocr_models()


@router.post("/process-chunk/", response_model=ProcessChunkResponse)
def process_chunk(req: ProcessChunkRequest):
    """ Process chunk of images function """
    result = AIModels.process_chunk(
        OCR_MODEL.get(req.ocr_model_type),
        FIND_TAGS_MODEL,
        req
    )
    return result


@router.post("/process-image/", response_model=ProcessImageResponse)
def process_image(req: ProcessImageRequest):
    """Rotate and process image function."""
    return AIModels.process_image(OCR_MODEL.get(req.ocr_model_type), FIND_TAGS_MODEL, req)
