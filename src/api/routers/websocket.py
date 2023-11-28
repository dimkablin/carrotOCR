"""Websocket"""

import json
from fastapi import APIRouter, WebSocket
from fastapi.encoders import jsonable_encoder

from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from src.api.routers.pipeline_router import process_chunk

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

    result = process_chunk(req)
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
