"""Upload files function service."""
import os.path

import cv2
import numpy as np

from src.api.models.upload_files import UploadFilesResponse
from src.utils.utils import get_abspath
from src.features.build_features import cut_image

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


async def upload_files_service(files, cut_image_flag=True) -> UploadFilesResponse:
    """Upload files to the server"""
    paths = []
    save_path = get_abspath("LOCAL_DATA")
    create_dir_if_not_exist(save_path)

    for file in files:
        filename = file.filename.split("/")[-1]

        # if file is IMAGE
        if check_extension(filename):
            path = os.path.join(save_path, filename)

            # read, cut and save image in LOCAL_DATA
            image = file.file.read()
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
            if cut_image_flag:
                image = cut_image(image)
            cv2.imwrite(path, image)

            paths.append(filename)

    return UploadFilesResponse(paths=paths)
