"""archive_chunk_service function service."""

from typing import Optional
import warnings
import zipfile
import os
from src.utils.utils import get_abspath
from src.db.processed_manager import ProcessedManager
from src.db.processed_structure import ProcessedStructure


async def archive_chunk_service(chunk_id: int,
                                filename: str = "DATA") -> Optional[str]:
    """archive_chunk_service function service."""

    path = get_abspath("LOCAL_DATA", str(chunk_id), "original")
    archive_path = get_abspath("LOCAL_DATA", str(chunk_id), filename + ".zip")

    if not os.path.exists(path):
        return None

    datas = ProcessedManager.get_data_by_chunk_id(chunk_id)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for data in datas:
            data = ProcessedStructure().from_db(data)

            if data.new_filename is None:
                warnings.warn("No new filename for data: " + str(data)[:50])
                continue

            old_path = get_abspath("LOCAL_DATA", str(chunk_id), "original", data.old_filename)
            new_filename = data.new_filename + "." + data.old_filename.split(".")[-1]

            if not os.path.exists(old_path):
                warnings.warn(f"File {old_path} not found.")
                continue

            zip_file.write(old_path, arcname=new_filename)

    return archive_path
