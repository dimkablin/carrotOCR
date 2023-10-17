"""Adding new filenames service."""
from src.api.models.add_filenames import AddFilenamesRequest
from src.db.processed_manager import ProcessedManager


async def add_filenames_service(req: AddFilenamesRequest):
    """Adding new filenames service."""
    for i in req.reqs:
        if not i.is_duplicate:
            ProcessedManager.insert_new_filename(i.filename, i.uid)
