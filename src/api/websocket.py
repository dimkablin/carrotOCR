"""Websocket"""

import json
from fastapi import APIRouter, WebSocket
from fastapi.encoders import jsonable_encoder

from src.api.services.process_chunk import process_chunk_service
from src.api.main import OCR_MODEL, FIND_TAGS_MODEL
from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse

router = APIRouter()

connections: dict[int, list[WebSocket]] = {}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, chunk_id: int, ocr_model_type: str):
    """websocket"""
    await websocket.accept()
    if chunk_id not in connections:
        connections[chunk_id] = []
    else:
        # Если уже существует подключение к этому chunkId, закрыть новое подключение
        if len(connections[chunk_id]) >= 1:
            await websocket.close()
            return

    connections[chunk_id].append(websocket)

    req = ProcessChunkRequest(chunk_id=chunk_id, ocr_model_type=ocr_model_type)

    result = await process_chunk_service(
            OCR_MODEL.get(ocr_model_type),
            FIND_TAGS_MODEL,
            req
        )
    await send_message_to_chunk(chunk_id, result)

    await websocket.close()
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


def get_websoket_router() -> APIRouter:
    """Return websocket app"""
    return router
