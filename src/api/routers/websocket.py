"""Websocket"""

import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, WebSocket
from fastapi.encoders import jsonable_encoder

from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from src.api.services.process_chunk import process_chunk_service

from src.models.ocr import OCRModelFactory
from src.models.find_tags import FindTags

executor = ThreadPoolExecutor(max_workers=5)

OCR_MODEL = OCRModelFactory()
FIND_TAGS_MODEL = FindTags()

websoket_router = APIRouter()
connections: dict[int, list[WebSocket]] = {}


@websoket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, chunk_id: int, ocr_model_type: str):
    """websocket"""
    await websocket.accept()
    if chunk_id not in connections:
        connections[chunk_id] = []
    else:
        # Если уже существует подключение к этому chunkId, закрыть новое подключение
        if len(connections[chunk_id]) >= 1:
            await websocket.close(code=4000, reason="Connection already exists for this chunk_id.")
            return

    connections[chunk_id].append(websocket)

    req = ProcessChunkRequest(chunk_id=chunk_id, ocr_model_type=ocr_model_type)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        process_chunk_service,
        OCR_MODEL.get(req.ocr_model_type),
        FIND_TAGS_MODEL,
        req
    )
    # result = await asyncio.create_task(process_chunk_service(
    #     OCR_MODEL.get(req.ocr_model_type),
    #     FIND_TAGS_MODEL,
    #     req
    # ))
    await send_message_to_chunk(chunk_id, result)

    await websocket.close(code=1000, reason="Connection closed successfully")
    connections[chunk_id].remove(websocket)
    if len(connections[chunk_id]) == 0:
        del connections[chunk_id]


async def send_message_to_chunk(chunk_id: int, message: ProcessChunkResponse):
    """Send message to chunk"""
    if chunk_id in connections:
        # Сериализуем ProcessChunkResponse в JSON
        json_message = json.dumps(jsonable_encoder(message))
        for connection in connections[chunk_id]:
            await connection.send_text(json_message)
