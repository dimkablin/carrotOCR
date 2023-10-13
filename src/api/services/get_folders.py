"""get_folders function controller."""
import os
from src.api.models.get_f_models import GetFRequest, GetFResponse


async def get_folders_service(req: GetFRequest) -> GetFResponse:
    """get_files function controller"""
    folders = [dir for dir in os.listdir(req.path) if os.path.isdir(os.path.join(req.path, dir))]

    return GetFResponse(paths=folders[:req.count])
