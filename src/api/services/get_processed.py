"""get_processed function service."""
from src.api.models.get_processed import GetProcessedResponse, GetProcessedRequest
from src.db.processed_manager import ProcessedManager
from src.utils.utils import bboxes2rect


async def get_processed_service(
        req: GetProcessedRequest,
        bbox2rect_flag=False) -> GetProcessedResponse:
    """get_processed service's main function ."""

    data = ProcessedManager.get_data_by_id(req.uid)
    result = GetProcessedResponse(
        path=data.path,
        old_filename=data.old_filename,
        new_filename=data.new_filename,
        tags=data.tags,
        text=data.text,
        bboxes=data.bboxes
    )

    if bbox2rect_flag:
        result.bboxes = bboxes2rect(result.bboxes)
    return result
