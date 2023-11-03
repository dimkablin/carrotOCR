"""fet_file function service."""
import os.path
from src.db.processed_manager import ProcessedManager
from src.utils.utils import get_abspath


async def get_file_service(uid: int):
    """get file service's main function."""
    data = ProcessedManager.get_data_by_id(uid)
    server_path = "http://213.171.5.243/api/"
    path = get_abspath("LOCAL_DATA", str(data.chunk_id), data.old_filename)

    if os.path.exists(path):
        return server_path+'/'.join(path.split('/')[-3:None])
