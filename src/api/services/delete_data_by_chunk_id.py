"""Clear data by chunk id"""


import os
from src.db.processed_manager import ProcessedManager
from src.utils.utils import get_abspath


async def delete_data_by_id_chunk_service(chunk_id: int) -> bool:
    """ Clear data by chunk id

    Args:
        chunk_id (int): chunk_id from LOCAL_DATA/chunk_id folder 

    Returns:
        bool: success of clearing data
    """

    path = get_abspath("LOCAL_DATA", str(chunk_id), "original")
    if not os.path.exists(path):
        return False

    return ProcessedManager().delete_data_by_chunk_id(chunk_id)
