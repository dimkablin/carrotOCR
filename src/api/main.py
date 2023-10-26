""" FastAPI connection """
from typing import List

from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.middleware.middleware import BackendMiddleware
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.api.services.get_processed import get_processed_service
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


MODEL = OCRModelFactoryProcessor("pytesseract")

app = FastAPI(
    openapi_tags=[{
        "name": "Backend API",
        "description": "Backend API router."
    }]
)
router = APIRouter()

app.add_middleware(BackendMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.mount("/LOCAL_DATA", StaticFiles(directory=get_abspath("LOCAL_DATA")), name="LOCAL_DATA")


@router.post("/process-image/", tags=["Backend API"], response_model=ProcessImageResponse)
async def process_image(req: ProcessImageRequest):
    """ Process image function """
    return await process_image_service(MODEL, req)


@router.post("/get-files/", tags=["Backend API"], response_model=GetFilesResponse)
async def get_files(req: GetFRequest):
    """Returning all directories in path."""
    return await get_files_service(req)


@router.post("/get-folders/", tags=["Backend API"], response_model=GetFoldersResponse)
async def get_folders(req: GetFRequest):
    """Returning all directories in path."""
    return await get_folders_service(req)


@router.post("/add-filenames/", tags=["Backend API"], response_model=None)
async def add_filenames(req: AddFilenamesRequest):
    """Adding new names of files to Database"""
    return await add_filenames_service(req)


@router.post("/upload-files/", tags=["Backend API"], response_model=UploadFilesResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Uploading files to the server."""
    return await upload_files_service(files)


@router.get("/get-models/", tags=["Backend API"], response_model=GetOCRModelsResponse)
async def get_ocr_models():
    """Return OCR Models ids and its names."""
    return await get_ocr_models_service()


@router.get("/get-file/", tags=["Backend API"])
async def get_file(uid: int):
    """Return file from static directory."""
    return await get_file_service(uid)


@router.post("/get-processed/", tags=["Backend API"], response_model=GetProcessedResponse)
async def get_processed(req: GetProcessedRequest):
    """Return data from processed table."""
    return await get_processed_service(req)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)  # 127.0.0.1:8000/api/..
