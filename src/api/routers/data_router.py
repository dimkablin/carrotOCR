"""Router that work with data"""

from fastapi import APIRouter
from src.api.services.delete_data_by_chunk_id import delete_data_by_id_chunk_service
from src.api.services.get_data_by_chunk_id import get_data_by_chunk_id_service
from src.api.services.get_files import get_files_service
from src.api.services.get_file import get_file_service
from src.api.services.get_folders import get_folders_service
from src.api.models.get_f import GetFRequest, GetFilesResponse, GetFoldersResponse

data_router = APIRouter()

@data_router.post("/get-files/", tags=["Work with data"], response_model=GetFilesResponse)
async def get_files(req: GetFRequest):
    """Returning all directories in path."""
    return await get_files_service(req)


@data_router.post("/get-folders/", tags=["Work with data"], response_model=GetFoldersResponse)
async def get_folders(req: GetFRequest):
    """Returning all directories in path."""
    return await get_folders_service(req)


@data_router.get("/get-file/", tags=["Work with data"])
async def get_file(uid: int):
    """Return file from static directory."""
    return await get_file_service(uid)


@data_router.get("/get-data-by-chunk-id/", tags=["Work with data"])
async def get_data_by_chunk_id(chunk_id: int):
    """Return data by chunk id"""
    return await get_data_by_chunk_id_service(chunk_id)


@data_router.post("/delete-data-by-chunk-id/", tags=["Work with data"], response_model=bool)
async def delete_data_by_chunk_id(chunk_id: int):
    """Clear data by chunk id"""
    return await delete_data_by_id_chunk_service(chunk_id)
