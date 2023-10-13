"""Upload files function service."""
import os.path
from src.api.models.upload_files_models import UploadFilesResponse

# available extension
EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"]


def check_extension(filename) -> bool:
    """Check available filename extension"""
    file_extension = os.path.splitext(filename)[-1].lower()
    return file_extension in EXTENSIONS


async def upload_files_service(files) -> UploadFilesResponse:
    """Upload files to the server"""
    paths = []

    for file in files:
        filename = file.filename
        path = os.path.join("", filename)

        with open(path, "wb") as wb_f:
            wb_f.write(file.file.read())
            paths.append(path)

    return UploadFilesResponse(paths=paths)
