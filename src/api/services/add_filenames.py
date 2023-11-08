"""Adding new filenames service."""
from src.api.models.add_filenames import AddFilenameRequest
from src.db.processed_manager import ProcessedManager


async def add_filenames_service(req: AddFilenameRequest):
    """Adding new filenames service."""
    if req.is_duplicate:
        return False

    return ProcessedManager.insert_new_filename(req.filename, req.uid)
