""" FastAPI connection """
from typing import List

from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.middleware.middleware import BackendMiddleware
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.api.services.archive_chunk import archive_chunk_service
from src.api.services.get_chunk_id import get_chunk_id_service
from src.api.services.get_processed import get_processed_service
from src.models.find_tags import FindTags
from src.utils.utils import get_abspath
from src.models.ocr.ocr import OCRModelFactoryProcessor

from src.api.services.add_filenames import add_filenames_service
from src.api.services.get_files import get_files_service
from src.api.services.get_file import get_file_service
from src.api.services.get_folders import get_folders_service
from src.api.services.get_ocr_models import get_ocr_models_service
from src.api.services.process_image import process_image_service
from src.api.services.upload_files import upload_files_service

from src.api.models.add_filenames import AddFilenamesRequest
from src.api.models.upload_files import UploadFilesResponse
from src.api.models.get_f import GetFRequest, GetFilesResponse, GetFoldersResponse
from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse
from src.api.models.get_ocr_models import GetOCRModelsResponse


OCR_MODEL = OCRModelFactoryProcessor("easyocr")
FIND_TAGS_MODEL = FindTags()


app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=[{
        "name": "Backend API",
        "description": "Backend API router."
    }]
)
router = APIRouter()

app.add_middleware(BackendMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.mount("/api/LOCAL_DATA", StaticFiles(directory=get_abspath("LOCAL_DATA")), name="LOCAL_DATA")


@router.get('/get-chunk-id/', tags=["Pipeline"], response_model=int)
async def get_chunk_id():
    """Return chunk id"""
    return await get_chunk_id_service()


@router.post("/upload-files/", tags=["Pipeline"], response_model=UploadFilesResponse)
async def upload_files(chunk_id: int, files: List[UploadFile] = File(...)):
    """Uploading files to the server."""
    return await upload_files_service(chunk_id, files)


@router.post("/process-image/", tags=["Pipeline"], response_model=ProcessImageResponse)
async def process_image(req: ProcessImageRequest):
    """ Process image function """
    return await process_image_service(OCR_MODEL, FIND_TAGS_MODEL, req)


@router.post("/get-processed/", tags=["Pipeline"], response_model=GetProcessedResponse)
async def get_processed(req: GetProcessedRequest):
    """Return data from processed table."""
    return await get_processed_service(req)


@router.post("/add-filenames/", tags=["Pipeline"], response_model=None)
async def add_filenames(req: AddFilenamesRequest):
    """Adding new names of files to Database"""
    return await add_filenames_service(req)


@router.post("/get-files/", tags=["Backend API"], response_model=GetFilesResponse)
async def get_files(req: GetFRequest):
    """Returning all directories in path."""
    return await get_files_service(req)


@router.post("/get-folders/", tags=["Backend API"], response_model=GetFoldersResponse)
async def get_folders(req: GetFRequest):
    """Returning all directories in path."""
    return await get_folders_service(req)


@router.get("/get-file/", tags=["Backend API"])
async def get_file(uid: int):
    """Return file from static directory."""
    return await get_file_service(uid)


@router.get('/archive-chunk/', tags=['Pipeline'], response_model=str)
async def archive_chunk(chunk_id: int, filename: str):
    """Archive chunk"""
    return await archive_chunk_service(chunk_id, filename)


@router.get("/get-ocr-models/", tags=["OCR"], response_model=GetOCRModelsResponse)
async def get_ocr_models():
    """Return OCR Models ids and its names."""
    return await get_ocr_models_service()


@router.get('/get-current-ocr-model/', tags=["OCR"], response_model=str)
async def get_current_ocr_model():
    """Return current OCR Model"""
    return OCR_MODEL.get_current_model()


@router.post('/change-ocr-model/', tags=["OCR"], response_model=None)
async def change_ocr_model(ocr_model_type: str):
    """Change OCR Model"""
    return OCR_MODEL.change_ocr_model(ocr_model_type)


app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
