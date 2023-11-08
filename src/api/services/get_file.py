"""fet_file function service."""
import os.path
from src.db.processed_manager import ProcessedManager
from src.utils.utils import get_abspath
from src.env import SERVER_PATH


async def get_file_service(uid: int):
    """get file service's main function."""
    data = ProcessedManager.get_data_by_id(uid)
    path = get_abspath("LOCAL_DATA", str(data.chunk_id), "edited", data.old_filename)

    index = path.find('LOCAL_DATA')

    return SERVER_PATH + path[index:]

    if os.path.exists(path):
        return SERVER_PATH + path[index:]
