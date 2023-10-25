"""fet_file function service."""
import os.path
from fastapi.responses import FileResponse
from src.db.processed_manager import ProcessedManager


async def get_file_service(uid: int):
    """get file service's main function."""
    path = ProcessedManager.get_data_by_id(uid).path
    if os.path.exists(path):
        return FileResponse(path)
