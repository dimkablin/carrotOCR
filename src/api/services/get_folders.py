"""get_folders function controller."""
import os
from src.api.models.get_f import GetFRequest, GetFoldersResponse


async def get_folders_service(req: GetFRequest) -> GetFoldersResponse:
    """get_files function controller"""

    folders = [dir for dir in os.listdir(req.path) if os.path.isdir(os.path.join(req.path, dir))]
    return GetFoldersResponse(folders=folders[:req.count])
