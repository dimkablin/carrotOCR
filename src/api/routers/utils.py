"""Utils for routers"""

import asyncio
import json
from fastapi.encoders import jsonable_encoder
from fastapi import WebSocket
from src.api.models.process_chunk import ProgressResponse


def send_progress_sync(connection: WebSocket, progress: ProgressResponse):
    """ Send progress of the process_chunk service"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(
            connection.send_text(json.dumps(jsonable_encoder(progress)))
        )
    finally:
        loop.close()
