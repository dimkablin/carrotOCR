"""ML model router"""

from fastapi import APIRouter
from src.models.find_tags import FindTags
from src.api.services.get_ocr_models import get_ocr_models_service
from src.api.models.get_ocr_models import GetOCRModelsResponse
from src.api.models.tags import GetTagsResponse, RemoveTagsResponse

ml_model_router = APIRouter()

@ml_model_router.get("/get-ocr-models/", tags=["OCR"], response_model=GetOCRModelsResponse)
def get_ocr_models():
    """Return OCR Models ids and its names."""
    return get_ocr_models_service()

@ml_model_router.get("/get-permatags/", tags=["Tags"], response_model=GetTagsResponse)
def get_permatags():
    """Return perma tags from database."""
    obj = FindTags()
    tags = obj.get_perma_tags()
    return GetTagsResponse(tags=tags)


@ml_model_router.get("/rm-permatag/", tags=["Tags"], response_model=RemoveTagsResponse)
def rm_permatags(tag:str):
    """Remove perma tag from database."""
    obj = FindTags()
    return RemoveTagsResponse(response=obj.rem_perma_tag(tag))


@ml_model_router.post("/set-permatag/", tags=["Tags"])
def add_permatag(tag:str):
    """Add perma tag to database. will return int"""
    obj = FindTags()
    return obj.add_perma_tag(tag)
