"""get_folders function service."""
import os
from src.api.models.get_f import GetFRequest, GetFoldersResponse


async def get_folders_service(req: GetFRequest) -> GetFoldersResponse:
    """get_folders function service"""
    path, dirname = os.path.split(req.path)
    folders = []
    if os.path.exists(path):
        for dir_ in os.listdir(path):
            if dir_.startswith(dirname):
                folders.append(dir_)
    if req.count != -1:
        folders = folders[:min(req.count, len(folders))]
    return GetFoldersResponse(folders=folders)
