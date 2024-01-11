""" Websocket router file"""

from fastapi import APIRouter, WebSocket
from src.api.routers.websocket import websocket_manager

websoket_router = APIRouter()

@websoket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, chunk_id: int, ocr_model_type: str):
    """Process Chunk WebSocket init"""
    await websocket_manager.connect(websocket, chunk_id, ocr_model_type)
    await websocket_manager.process_chunk(chunk_id, ocr_model_type)
    await websocket_manager.disconnect(websocket, chunk_id)
