"""archive_chunk_service function service."""

from typing import Optional
import warnings
from urllib.parse import unquote
import zipfile
import os
from src.env import SERVER_PATH, DATA_PATH
from src.db.processed_manager import ProcessedManager
from src.db.structures.processed_structure import ProcessedStructure


def archive_chunk_service(
        chunk_id: int,
        filename: str = "DATA") -> Optional[str]:
    """archive_chunk_service function service."""
    filename = unquote(filename)

    path = os.path.join(DATA_PATH, str(chunk_id))
    archive_path = os.path.join(DATA_PATH, str(chunk_id), filename + ".zip")

    if not os.path.exists(path):
        return None

    datas = ProcessedManager.get_data_by_chunk_id(chunk_id)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for data in datas:
            data = ProcessedStructure().from_db(data)

            new_filename = data.new_filename + "." + data.old_filename.split(".")[-1]
            old_path = os.path.join(DATA_PATH, str(chunk_id), data.old_filename)

            if not os.path.exists(old_path):
                warnings.warn(f"File {old_path} not found.")
                continue

            zip_file.write(old_path, arcname=new_filename)

    return SERVER_PATH + archive_path[path.find(DATA_PATH):]
