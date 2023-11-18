""" Connection Manager """

from fastapi import WebSocket
from pydantic import BaseModel


class ConnectionManager:
    """The class that contains websockets and handle them."""
    def __init__(self):
        """  """
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """ Adding a connetion 

        Args:
            websocket (WebSocket): _description_
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """ Deleting a connection

        Args:
            websocket (WebSocket): _description_
        """
        self.active_connections.remove(websocket)

    async def send_result(self, result: BaseModel, websocket: WebSocket):
        """ 

        Args:
            message (str): _description_
            websocket (WebSocket): _description_
        """
        await websocket.send_json(result.model_dump())
