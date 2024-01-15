"""Clear data by chunk id"""

from src.db.processed_manager import ProcessedManager


def delete_data_by_id_chunk_service(chunk_id: int) -> bool:
    """ Clear data by chunk id

    Args:
        chunk_id (int): chunk_id from LOCAL_DATA/chunk_id folder 

    Returns:
        bool: success of clearing data
    """

    return ProcessedManager().delete_data_by_chunk_id(chunk_id)
