"""fet_file function service."""
import os
from src.db.processed_manager import ProcessedManager
from src.env import SERVER_PATH


def get_file_service(uid: int):
    """get file service's main function."""
    data = ProcessedManager.get_data_by_id(uid)
    path = SERVER_PATH + os.path.join('LOCAL_DATA', str(data.chunk_id), data.old_filename)

    return path
