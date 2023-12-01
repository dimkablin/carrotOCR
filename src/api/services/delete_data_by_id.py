"""_summary_"""


from src.db.processed_manager import ProcessedManager


def delete_data_by_id_service(uid: int) -> bool:
    """Delete data from the database by id."""
    return ProcessedManager.delete_data_by_id(uid)
