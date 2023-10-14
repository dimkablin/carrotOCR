"""get_folders function service."""
import os
from src.api.models.get_f import GetFRequest, GetFoldersResponse


async def get_folders_service(req: GetFRequest) -> GetFoldersResponse:
    """get_files function service"""
    path, dirname = os.path.split(req.path)
    folders = []
    if os.path.exists(path):
        for dir_ in os.listdir(path):
            if os.path.isdir(os.path.join(path, dir_)) and dir_.startswith(dirname):
                folders.append(dir_)

    return GetFoldersResponse(folders=folders[:req.count])
