"""Websocket and initialization of ai_models"""

from concurrent.futures import ThreadPoolExecutor
import asyncio
import json
from typing import List

from fastapi.encoders import jsonable_encoder

from fastapi import WebSocket
from pydantic import BaseModel

from src.ai_models.ocr import OCR_MODEL
from src.ai_models.find_tags import FIND_TAGS_MODEL
from src.api.models.ai_models import ProcessChunkRequest, ProcessChunkResponse


from src.api.models.ai_models import ProgressResponse
from src.api.crud.ai_models import AIModels


executor = ThreadPoolExecutor(max_workers=5)


class WebSocketManager:
    """WebSocket Class"""
    def __init__(self, ocr_model, find_tags_model):
        self.connections: dict[int, list[WebSocket]] = {}
        self.ocr_model = ocr_model
        self.find_tags_model = find_tags_model

    async def connect(self, websocket: WebSocket, chunk_id: int, ocr_model_type: str):
        """Handle WebSocket connection"""
        await websocket.accept()

        if chunk_id not in self.connections:
            self.connections[chunk_id] = []
            asyncio.create_task(self.send_pong(websocket))
        else:
            if len(self.connections[chunk_id]) >= 1:
                await websocket.close(
                    code=4000,
                    reason="Connection already exists for this chunk_id."
                )
                return

        self.connections[chunk_id].append(websocket)

    async def send_pong(self, websocket: WebSocket):
        """Send 'pong' message every 10 seconds"""
        while True:
            try:
                await asyncio.sleep(10)
                await websocket.send_json({"action": "pong"})
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in send_pong: {e}")
                break

    async def disconnect(self, websocket: WebSocket, chunk_id: int):
        """Handle WebSocket disconnection"""
        await websocket.close(code=1000, reason="Connection closed successfully")
        self.connections[chunk_id].remove(websocket)
        if len(self.connections[chunk_id]) == 0:
            del self.connections[chunk_id]

    async def process_chunk(self, chunk_id: int, ocr_model_type: str):
        """Process chunk and send result to connected clients"""
        req = ProcessChunkRequest(chunk_id=chunk_id, ocr_model_type=ocr_model_type)

        loop = asyncio.get_event_loop()

        tqdm = UpdateProgress(connections=self.connections[chunk_id])
        result = await loop.run_in_executor(
            executor,
            AIModels.process_chunk,
            self.ocr_model.get(req.ocr_model_type),
            self.find_tags_model,
            req,
            tqdm
        )
        await self.send_message_to_chunk(chunk_id, result)

    async def send_message_to_chunk(self, chunk_id: int, message: ProcessChunkResponse):
        """Send message to chunk"""
        if chunk_id in self.connections:
            json_message = json.dumps(jsonable_encoder(message))
            for connection in self.connections[chunk_id]:
                await connection.send_text(json_message)

    @staticmethod
    def send_json(connection: WebSocket, message: BaseModel):
        """ Send progress of the process_chunk service"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(
                connection.send_text(json.dumps(jsonable_encoder(message)))
            )
        finally:
            loop.close()


class UpdateProgress:
    """Class to send progress via websocket"""
    def __init__(self, connections: List[WebSocket], length: int = 0, message: str = ""):
        self.i = 0
        self.length = length
        self.connections = connections
        self.message = message

    def update(self):
        """ Update progress and senf it via socket"""
        self.i += 1

        if self.connections is not None:
            for connection in self.connections:
                WebSocketManager.send_json(
                    connection,
                    ProgressResponse(
                        iter=self.i,
                        length=self.length,
                        message=self.message
                    )
                )


websocket_manager = WebSocketManager(OCR_MODEL, FIND_TAGS_MODEL)
