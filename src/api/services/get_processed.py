"""get_processed function service."""
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.db.processed_manager import ProcessedManager
from src.utils.utils import bboxes2rect


async def get_processed_service(req: GetProcessedRequest) -> GetProcessedResponse:
    """get_processed service's main function ."""

    data = ProcessedManager.get_data_by_id(req.uid)
    result = GetProcessedResponse(
        chunk_id=data.chunk_id,
        old_filename=data.old_filename,
        new_filename=data.new_filename,
        tags=data.tags,
        text=data.text,
        bboxes=bboxes2rect(data.bboxes)
    )
    return result