"""fet_file function service."""
import os.path
from src.db.processed_manager import ProcessedManager
from src.utils.utils import get_abspath


async def get_file_service(uid: int):
    """get file service's main function."""
    data = ProcessedManager.get_data_by_id(uid)
    chunk_id = data.chunk_id
    old_filename = data.old_filename
    path = get_abspath("LOCAL_DATA", chunk_id, old_filename)

    if os.path.exists(path):
        return path
