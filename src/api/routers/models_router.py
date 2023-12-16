"""ML model router"""

from fastapi import APIRouter
from src.db.grouptags_manager import GrouptagsManager
from src.db.permatags_manager import PermatagsManager
from src.db.structures.permatags_structure import PermatagsStructure
from src.api.services.get_ocr_models import get_ocr_models_service
from src.api.models.get_ocr_models import GetOCRModelsResponse
from src.api.models.tags import GetTagsResponse, GrouptagsResponse, RemoveTagsResponse

ml_model_router = APIRouter()

@ml_model_router.get("/get-ocr-models/", tags=["OCR"], response_model=GetOCRModelsResponse)
def get_ocr_models():
    """Return OCR Models ids and its names."""
    return get_ocr_models_service()

@ml_model_router.get("/get-permatags/", tags=["Tags"], response_model=GetTagsResponse)
def get_permatags():
    """Return perma tags from database."""
    tags = PermatagsManager.get_all_data()
    return GetTagsResponse(tags=tags)

@ml_model_router.get("/get-permatags/", tags=["Tags"], response_model=GetTagsResponse)
def get_permatags_by_group(group: int):
    """Return perma tags from database."""
    tags = PermatagsManager.get_data_by_group(group)
    return GetTagsResponse(tags=tags)


@ml_model_router.get("/rm-permatag/", tags=["Tags"], response_model=RemoveTagsResponse)
def rm_permatags(tag: str):
    """Remove perma tag from database."""
    data = PermatagsManager.delete_data_by_tag(tag)
    return RemoveTagsResponse(response=data)


@ml_model_router.post("/set-permatag/", tags=["Tags"])
def add_permatag(tag:str, group: str):
    """Add perma tag to database. will return int"""
    data = PermatagsStructure(tag=tag, group=group)
    return PermatagsManager.insert_data(data)


@ml_model_router.post("/get-group-tags/", tags=["Tags"])
def get_grouptags() -> list[GrouptagsResponse]:
    """Return group of tags"""
    data = GrouptagsManager.get_all_data()