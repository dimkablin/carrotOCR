"""Pipeline router"""
from typing import List

from fastapi import APIRouter, UploadFile, File
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.api.models.process_image import ProcessImageResponse, ProcessImageRequest
from src.api.routers.websocket import OCR_MODEL, FIND_TAGS_MODEL

from src.api.services.archive_chunk import archive_chunk_service
from src.api.services.delete_data_by_id import delete_data_by_id_service
from src.api.services.get_chunk_id import get_chunk_id_service
from src.api.services.get_processed import get_processed_service
from src.api.services.process_image import process_image_service

from src.api.services.add_filenames import add_filenames_service
from src.api.services.process_chunk import process_chunk_service
from src.api.services.upload_files import upload_files_service

from src.api.models.add_filenames import AddFilenameRequest
from src.api.models.upload_files import UploadFilesResponse
from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse

pipeline_router = APIRouter()


@pipeline_router.get('/get-chunk-id/', tags=["Pipeline"], response_model=int)
def get_chunk_id():
    """Return chunk id"""
    return get_chunk_id_service()


@pipeline_router.post("/upload-files/", tags=["Pipeline"], response_model=UploadFilesResponse)
def upload_files(chunk_id: int, files: List[UploadFile] = File(...)):
    """Uploading files to the server."""
    return upload_files_service(chunk_id, files)

@pipeline_router.post("/process-chunk/", tags=["Pipeline"], response_model=ProcessChunkResponse)
def process_chunk(req: ProcessChunkRequest):
    """ Process chunk of images function """
    result = process_chunk_service(
        OCR_MODEL.get(req.ocr_model_type),
        FIND_TAGS_MODEL,
        req
    )
    return result

@pipeline_router.post("/process-image/", tags=["Pipeline"], response_model=ProcessImageResponse)
def process_image(req: ProcessImageRequest):
    """Rotate and process image function."""
    return process_image_service(OCR_MODEL.get(req.ocr_model_type), FIND_TAGS_MODEL, req)

@pipeline_router.post("/get-data-by-id/", tags=["Pipeline"], response_model=GetProcessedResponse)
def get_processed(req: GetProcessedRequest):
    """Return data from processed table by id."""
    return get_processed_service(req)


@pipeline_router.post("/delte-data-by-id/", tags=["Pipeline"], response_model=None)
def delete_data_by_id(uid: int):
    """Delete data from the database by id."""
    return delete_data_by_id_service(uid)


@pipeline_router.post("/add-filename/", tags=["Pipeline"], response_model=bool)
def add_filenames(req: AddFilenameRequest):
    """Adding new names of files to Database"""
    return add_filenames_service(req)

@pipeline_router.get('/archive-chunk/', tags=['Pipeline'], response_model=str)
def archive_chunk(chunk_id: int, filename: str):
    """Archive chunk"""
    return archive_chunk_service(chunk_id, filename)
