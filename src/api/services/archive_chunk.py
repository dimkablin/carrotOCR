"""archive_chunk_service function service."""

from typing import Optional
import zipfile
import os
from src.utils.utils import get_abspath
from src.db.processed_manager import ProcessedManager
from src.db.processed_structure import ProcessedStructure


def rename_files(chunk_id: int) -> None:
    """rename_files function service."""
    datas = ProcessedManager.get_data_by_chunk_id(chunk_id)
    for data in datas:
        data = ProcessedStructure().from_db(data)
        if data.new_filename is not None:
            old_path = get_abspath("LOCAL_DATA", str(chunk_id), data.old_filename)

            new_filename = data.new_filename + "." + data.old_filename.split(".")[-1]
            new_path = get_abspath("LOCAL_DATA", str(chunk_id), new_filename)

            os.rename(old_path, new_path)

            
    return None

def archive_folder(folder_path, archive_path):
    """Archive the contents of a folder into a zip file."""
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)


async def archive_chunk_service(chunk_id: int, 
                                remove_folder: bool = False, 
                                filename: str="DATA") -> Optional[str]:
    """archive_chunk_service function service."""

    folder_path = get_abspath("LOCAL_DATA", str(chunk_id))
    archive_path = filename + ".zip"

    # Rename files in LCOAL_DATA/chunk_id folder
    rename_files(chunk_id)

    if os.path.exists(folder_path):
        # Archive files in LCOAL_DATA/chunk_id folder
        archive_folder(folder_path, archive_path)

        # Remove LCOAL_DATA/chunk_id folder if it needs
        if remove_folder:
            os.remove(folder_path)

        return archive_path
    return None
