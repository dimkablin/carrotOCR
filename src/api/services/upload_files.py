"""Upload files function service."""
import os.path

from src.api.models.upload_files import UploadFilesResponse
from src.utils.utils import get_abspath

# available extension
EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]


def check_extension(filename) -> bool:
    """Check available filename extension"""
    file_extension = os.path.splitext(filename)[-1].lower()
    return file_extension in EXTENSIONS


def create_dir_if_not_exist(path_: str) -> None:
    """Creating directory if it doesn't exist."""
    if not os.path.exists(path_):
        os.mkdir(path_)


async def upload_files_service(chunk_id, files) -> UploadFilesResponse:
    """Upload files to the server"""
    paths = []
    save_path = get_abspath("LOCAL_DATA", str(chunk_id))
    create_dir_if_not_exist(save_path)

    for file in files:
        filename = file.filename.split('/')[-1]
        if check_extension(filename):
            path = os.path.join(save_path, filename)

            with open(path, "wb") as wb_f:
                wb_f.write(file.file.read())
                paths.append(path)

    return UploadFilesResponse(paths=paths)
