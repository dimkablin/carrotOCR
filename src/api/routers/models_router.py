"""ML model router"""

from fastapi import APIRouter
from src.db.grouptags_manager import GrouptagsManager
from src.db.permatags_manager import PermatagsManager
from src.db.structures.permatags_structure import PermatagsStructure
from src.api.services.get_ocr_models import get_ocr_models_service
from src.api.models.get_ocr_models import GetOCRModelsResponse
from src.api.models.tags import GrouptagsResponse, GetPermatagsResponse, RemoveTagsResponse

ml_model_router = APIRouter()

@ml_model_router.get("/get-ocr-models/", tags=["OCR"], response_model=GetOCRModelsResponse)
def get_ocr_models():
    """Return OCR Models ids and its names."""
    return get_ocr_models_service()


@ml_model_router.get("/get-permatags/", tags=["Tags"], response_model=GetPermatagsResponse)
def get_permatags():
    """Return perma tags from database."""
    return PermatagsManager.get_all_data()

@ml_model_router.get("/get-permatags-by-group/", tags=["Tags"], response_model=GetPermatagsResponse)
def get_permatags_by_group(group_id: int):
    """Return perma tags from database."""
    return PermatagsManager.get_data_by_group(group_id)


@ml_model_router.get("/rm-permatag/", tags=["Tags"], response_model=RemoveTagsResponse)
def rm_permatags(tag: str, group_id: int):
    """Remove perma tag from database."""
    data = PermatagsManager.delete_data_by_tag(tag, group_id)
    return RemoveTagsResponse(response=data)


@ml_model_router.get("/rm-permatag-by-id/", tags=["Tags"], response_model=RemoveTagsResponse)
def rm_permatags_by_id(uid: int):
    """Remove perma tag from database."""
    data = PermatagsManager.delete_data_by_id(uid)
    return RemoveTagsResponse(response=data)


@ml_model_router.post("/set-permatag/", tags=["Tags"])
def add_permatag(tag:str, group_id: int):
    """Add perma tag to database. will return int"""
    data = PermatagsStructure(tag=tag, group_id=group_id)
    return PermatagsManager.insert_data(data)


@ml_model_router.post("/get-group-tags/", tags=["Tags"])
def get_grouptags() -> list[GrouptagsResponse]:
    """Return group of tags"""
    data = GrouptagsManager.get_all_data()
    return data
