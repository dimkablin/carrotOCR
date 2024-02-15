"""Router that work with data"""
from typing import List
from pkg_resources import get_distribution
from fastapi import APIRouter, File, UploadFile

from src.api.crud.data import Data
from src.api.models.data import *


router = APIRouter()


@router.post("/get-files/", response_model=GetFilesResponse)
def get_files(req: GetFRequest):
    """Returning all directories in path."""
    return Data.get_files(req)


@router.post("/get-folders/", response_model=GetFoldersResponse)
def get_folders(req: GetFRequest):
    """Returning all directories in path."""
    return Data.get_folders(req)


@router.get("/get-file/")
def get_file(uid: int, pdf_id: int):
    """Return file from static directory."""
    return Data.get_file(uid, pdf_id)


@router.get('/get-chunk-id/', response_model=int)
def get_chunk_id():
    """Return chunk id"""
    return Data.get_chunk_id()


@router.get("/get-files-extension/", response_model=set)
def get_files_extension():
    """Return all file extensions"""
    return FILE_EXTENSIONS


@router.get("/get-images-extension/", response_model=set)
def get_images_extension():
    """Return all images extensions"""
    return IMAGE_EXTENSIONS


@router.get("/get-file-type/", response_model=str)
def get_file_type(extension: str):
    """Return file type"""
    if extension in FILE_EXTENSIONS:
        return "file"
    if extension in IMAGE_EXTENSIONS:
        return "image"
    return "unknown"


@router.post("/upload-files/", response_model=UploadFilesResponse)
def upload_files(chunk_id: int, files: List[UploadFile] = File(...)):
    """Uploading files to the server."""
    return Data.upload_files(chunk_id, files)


@router.get('/archive-chunk/', response_model=str)
def archive_chunk(chunk_id: int, filename: str):
    """Archive chunk"""
    return Data.archive_chunk(chunk_id, filename)


@router.get("/get-backend-version/", response_model=str)
def get_backend_version():
    """Return version of backend."""
    distribution = get_distribution("src")
    return distribution.version
