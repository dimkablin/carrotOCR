"""get_files function controller."""
import os
from src.api.models.get_f import GetFRequest, GetFilesResponse


def get_files_service(req: GetFRequest) -> GetFilesResponse:
    """get_files function controller"""
    if not os.path.exists(req.path):
        return GetFilesResponse(files=[])

    files = [file for file in os.listdir(req.path) if os.path.isfile(os.path.join(req.path, file))]

    if req.count != -1:
        files = files[:min(req.count, len(files))]
    return GetFilesResponse(files=files)
