"""get_files function controller."""
import os
from src.api.models.get_f_models import GetFRequest, GetFResponse


async def get_files_service(req: GetFRequest) -> GetFResponse:
    """get_files function controller"""
    files = [file for file in os.listdir(req.path) if os.path.isfile(os.path.join(req.path, file))]

    return GetFResponse(paths=files[:req.count])
