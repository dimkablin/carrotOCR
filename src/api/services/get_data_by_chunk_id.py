""" get data by chunk id """


from typing import Any
from src.db.processed_manager import ProcessedManager
from src.db.processed_structure import ProcessedStructure


def get_data_by_chunk_id_service(chunk_id: int) -> list[Any]:
    """Return data by chunk id"""
    datas = ProcessedManager.get_data_by_chunk_id(chunk_id)
    datas = [ProcessedStructure().from_db(data) for data in datas]

    for data in datas:
        data.tags = None
        data.bboxes = None
        data.text = None

    return datas
