""" FastAPI connection """
from typing import List
import logging
import json
import asyncio

from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from src.api.middleware.middleware import BackendMiddleware
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.api.models.process_image import ProcessImageResponse, ProcessImageRequest
from src.api.services.archive_chunk import archive_chunk_service
from src.api.services.delete_data_by_chunk_id import delete_data_by_id_chunk_service
from src.api.services.delete_data_by_id import delete_data_by_id_service
from src.api.services.get_chunk_id import get_chunk_id_service
from src.api.services.get_data_by_chunk_id import get_data_by_chunk_id_service
from src.api.services.get_processed import get_processed_service
from src.api.services.process_image import process_image_service
from src.utils.utils import get_abspath

from src.models.ocr.ocr import OCRModelFactory
from src.models.find_tags import FindTags
from src.api.router import ConnectionManager

from src.api.services.add_filenames import add_filenames_service
from src.api.services.get_files import get_files_service
from src.api.services.get_file import get_file_service
from src.api.services.get_folders import get_folders_service
from src.api.services.get_ocr_models import get_ocr_models_service
from src.api.services.process_chunk import process_chunk_service
from src.api.services.upload_files import upload_files_service
from src.api.websocket import get_websoket_app

from src.api.models.add_filenames import AddFilenameRequest
from src.api.models.upload_files import UploadFilesResponse
from src.api.models.get_f import GetFRequest, GetFilesResponse, GetFoldersResponse
from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from src.api.models.get_ocr_models import GetOCRModelsResponse

OCR_MODEL = OCRModelFactory()
FIND_TAGS_MODEL = FindTags()

connection_manager = ConnectionManager()

# LOGGING CONFIG SETTING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logging.info("Running server.")

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


@router.post("/process-chunk/", tags=["Pipeline"], response_model=ProcessChunkResponse)
async def process_chunk(req: ProcessChunkRequest, websocket: WebSocket):
    """ Process chunk of images function """
    await connection_manager.connect(websocket)

    try:
        result = await process_chunk_service(
            OCR_MODEL.get(req.ocr_model_type),
            FIND_TAGS_MODEL,
            req
        )
        await connection_manager.send_result(result, websocket)
    finally:
        connection_manager.disconnect(websocket)
    return result


@router.post("/process-image/", tags=["Pipeline"], response_model=ProcessImageResponse)
async def process_image(req: ProcessImageRequest):
    """Rotate and process image function."""
    return await process_image_service(OCR_MODEL.get(req.ocr_model_type), FIND_TAGS_MODEL, req)


@router.post("/get-data-by-id/", tags=["Pipeline"], response_model=GetProcessedResponse)
async def get_processed(req: GetProcessedRequest):
    """Return data from processed table by id."""
    return await get_processed_service(req)


@router.post("/delte-data-by-id/", tags=["Pipeline"], response_model=None)
async def delete_data_by_id(uid: int):
    """Delete data from the database by id."""
    return await delete_data_by_id_service(uid)


@router.post("/add-filename/", tags=["Pipeline"], response_model=bool)
async def add_filenames(req: AddFilenameRequest):
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

@router.get("/get-data-by-chunk-id/", tags=["Backend API"])
async def get_data_by_chunk_id(chunk_id: int):
    """Return data by chunk id"""
    return await get_data_by_chunk_id_service(chunk_id)


@router.post("/delete-data-by-chunk-id/", tags=["Backend API"], response_model=bool)
async def delete_data_by_chunk_id(chunk_id: int):
    """Clear data by chunk id"""
    return await delete_data_by_id_chunk_service(chunk_id)


@router.get('/archive-chunk/', tags=['Pipeline'], response_model=str)
async def archive_chunk(chunk_id: int, filename: str):
    """Archive chunk"""
    return await archive_chunk_service(chunk_id, filename)


@router.get("/get-ocr-models/", tags=["OCR"], response_model=GetOCRModelsResponse)
async def get_ocr_models():
    """Return OCR Models ids and its names."""
    return await get_ocr_models_service()

connections: dict[int, list[WebSocket]] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, chunkId: int, ocr_model_type: str):
    await websocket.accept()
    if chunkId not in connections:
        connections[chunkId] = []
    else:
        # Если уже существует подключение к этому chunkId, закрыть новое подключение
        if len(connections[chunkId]) >= 1:
            await websocket.close()
            return

    connections[chunkId].append(websocket)

    req = ProcessChunkRequest(chunk_id=chunkId, ocr_model_type=ocr_model_type)

    result = await process_chunk_service(
            OCR_MODEL.get(ocr_model_type),
            FIND_TAGS_MODEL,
            req
        )
    await send_message_to_chunk(chunkId, result)

    await websocket.close()
    connections[chunkId].remove(websocket)
    if len(connections[chunkId]) == 0:
        del connections[chunkId]

async def send_message_to_chunk(chunkId: int, message: ProcessChunkResponse):
    if chunkId in connections:
        # Сериализуем ProcessChunkResponse в JSON
        json_message = json.dumps(jsonable_encoder(message))
        for connection in connections[chunkId]:
            await connection.send_text(json_message)

app.include_router(router, prefix="/api")
