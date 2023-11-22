"""Pipeline router"""
from typing import List

from fastapi import APIRouter, UploadFile, File
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.api.models.process_image import ProcessImageResponse, ProcessImageRequest
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

from src.models.ocr.ocr import OCRModelFactory
from src.models.find_tags import FindTags

OCR_MODEL = OCRModelFactory()
FIND_TAGS_MODEL = FindTags()
pipeline_router = APIRouter()


@pipeline_router.get('/get-chunk-id/', tags=["Pipeline"], response_model=int)
async def get_chunk_id():
    """Return chunk id"""
    return await get_chunk_id_service()


@pipeline_router.post("/upload-files/", tags=["Pipeline"], response_model=UploadFilesResponse)
async def upload_files(chunk_id: int, files: List[UploadFile] = File(...)):
    """Uploading files to the server."""
    return await upload_files_service(chunk_id, files)


@pipeline_router.post("/process-chunk/", tags=["Pipeline"], response_model=ProcessChunkResponse)
async def process_chunk(req: ProcessChunkRequest):
    """ Process chunk of images function """
    result = await process_chunk_service(
        OCR_MODEL.get(req.ocr_model_type),
        FIND_TAGS_MODEL,
        req
    )
    return result


@pipeline_router.post("/process-image/", tags=["Pipeline"], response_model=ProcessImageResponse)
async def process_image(req: ProcessImageRequest):
    """Rotate and process image function."""
    return await process_image_service(OCR_MODEL.get(req.ocr_model_type), FIND_TAGS_MODEL, req)


@pipeline_router.post("/get-data-by-id/", tags=["Pipeline"], response_model=GetProcessedResponse)
async def get_processed(req: GetProcessedRequest):
    """Return data from processed table by id."""
    return await get_processed_service(req)


@pipeline_router.post("/delte-data-by-id/", tags=["Pipeline"], response_model=None)
async def delete_data_by_id(uid: int):
    """Delete data from the database by id."""
    return await delete_data_by_id_service(uid)


@pipeline_router.post("/add-filename/", tags=["Pipeline"], response_model=bool)
async def add_filenames(req: AddFilenameRequest):
    """Adding new names of files to Database"""
    return await add_filenames_service(req)

@pipeline_router.get('/archive-chunk/', tags=['Pipeline'], response_model=str)
async def archive_chunk(chunk_id: int, filename: str):
    """Archive chunk"""
    return await archive_chunk_service(chunk_id, filename)
