"""archive_chunk_service function service."""

from typing import Optional
import zipfile
import os
from src.utils.utils import get_abspath


def archive_folder(filepath, filename) -> None:
    """archive_folder function service."""
    with zipfile.ZipFile(filename, "w") as zip_file:
        for root, dirs, files in os.walk(filepath):
            for file in files:
                zip_file.write(os.path.join(root, file))


async def archive_chunk_service(chunk_id: int, remove_folder=False) -> Optional[str]:
    """archive_chunk_service function service."""
    dirname = str(chunk_id)
    path = get_abspath("LOCAL_DATA", dirname)

    if os.path.exists(path):
        archive_path = path + ".zip"
        archive_folder(path, archive_path)

        if remove_folder:
            os.remove(path)
        return archive_path
    return None
