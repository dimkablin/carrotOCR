"""Endpoint for database functions"""
from fastapi import APIRouter

from src.api.crud.database import Database
from src.api.models.database import *
from src.db.grouptags_manager import GrouptagsManager
from src.db.permatags_manager import PermatagsManager
from src.db.structures.permatags_structure import PermatagsStructure


router = APIRouter()


@router.get("/get-data-by-chunk-id/")
def get_data_by_chunk_id(chunk_id: int):
    """Return data by chunk id"""
    return Database.get_data_by_chunk_id(chunk_id)


@router.post("/delete-data-by-chunk-id/", response_model=bool)
def delete_data_by_chunk_id(chunk_id: int):
    """Clear data by chunk id"""
    return Database.delete_data_by_id_chunk(chunk_id)


@router.post("/delete-data-by-id/", response_model=None)
def delete_data_by_id(uid: int):
    """Delete data from the database by id."""
    return Database.delete_data_by_id(uid)


@router.get("/get-permatags/", response_model=GetPermatagsResponse)
def get_permatags():
    """Return perma tags from database."""
    return PermatagsManager.get_all_data()


@router.get("/get-permatags-by-group/", response_model=GetPermatagsResponse)
def get_permatags_by_group(group_id: int):
    """Return perma tags from database."""
    return PermatagsManager.get_data_by_group(group_id)


@router.get("/rm-permatag/", response_model=RemoveTagsResponse)
def rm_permatags(tag: str, group_id: int):
    """Remove perma tag from database."""
    data = PermatagsManager.delete_data_by_tag(tag, group_id)
    return RemoveTagsResponse(response=data)


@router.get("/rm-permatag-by-id/", response_model=RemoveTagsResponse)
def rm_permatags_by_id(uid: int):
    """Remove perma tag from database."""
    data = PermatagsManager.delete_data_by_id(uid)
    return RemoveTagsResponse(response=data)


@router.post("/set-permatag/")
def add_permatag(tag:str, group_id: int):
    """Add perma tag to database. will return int"""
    data = PermatagsStructure(tag=tag, group_id=group_id)
    return PermatagsManager.insert_data(data)


@router.post("/get-group-tags/")
def get_grouptags() -> list[GrouptagsResponse]:
    """Return group of tags"""
    data = GrouptagsManager.get_all_data()
    data.append(GrouptagsResponse(
        name="Дата",
        is_local=True
    ))
    return data


@router.post("/get-data-by-id/", response_model=GetProcessedResponse)
def get_processed(req: GetProcessedRequest):
    """Return data from processed table by id."""
    return Database.get_processed(req)


@router.post("/add-filename/", response_model=bool)
def add_filenames(req: AddFilenameRequest):
    """Adding new names of files to Database"""
    return Database.add_filenames(req)
