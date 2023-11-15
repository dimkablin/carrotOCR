from fastapi import WebSocket, FastAPI
from src.api.services.process_chunk import process_chunk_service
from src.models.ocr.ocr import OCRModelFactory
from src.models.find_tags import FindTags
from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

OCR_MODEL = OCRModelFactory()
FIND_TAGS_MODEL = FindTags()

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

def get_websoket_app():
    return app