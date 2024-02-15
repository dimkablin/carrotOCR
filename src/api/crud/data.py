"""Crud for functions working with os."""
import os
from typing import Optional, List
import warnings
from urllib.parse import unquote
import zipfile
import fitz

from src.db.processed_manager import ProcessedManager
from src.db.files_manager import FilesManager
from src.db.structures.file_structure import FileStructure
from src.env import SERVER_PATH, DATA_PATH
from src.api.models.data import *
from src.features import extract_features as pp
from src.utils.utils import create_dir


class Data:
    """Functions working with os class"""

    @staticmethod
    def get_file(uid: int, pdf_id: int = None):
        """get file service's main function."""
        data = ProcessedManager.get_data_by_id(uid)
        path = SERVER_PATH + os.path.join('LOCAL_DATA', str(data.chunk_id))

        if pdf_id is not None:
            path = os.path.join(path, str(pdf_id), data.old_filename)
        else:
            path = os.path.join(path, data.old_filename)

        return path

    @staticmethod
    def get_files(req: GetFRequest) -> GetFilesResponse:
        """get_files function controller"""
        if not os.path.exists(req.path):
            return GetFilesResponse(files=[])

        files = []
        for file in os.listdir(req.path):
            file_path = os.path.join(req.path, file)
            if os.path.isfile(file_path) and pp.check_extension(file_path, IMAGE_EXTENSIONS):
                files.append(file)

        if req.count != -1:
            files = files[:min(req.count, len(files))]
        return GetFilesResponse(files=files)

    @staticmethod
    def pdf_to_images(file_path: str, save_path: str, dpi: int = 200) -> List[str]:
        """Convert pdf to images"""
        paths = []

        for page in fitz.open(file_path):
            image = page.get_pixmap(matrix=fitz.Matrix(dpi/72.0, dpi/72.0))

            # Save the image as PNG
            image_path = os.path.join(
                save_path,
                f"page_{page.number}.png"
            )
            image.save(image_path)
            paths.append(image_path)

        return paths

    @staticmethod
    def upload_files(chunk_id, files) -> UploadFilesResponse:
        """Upload images to the server"""
        paths = []
        save_path = os.path.join(DATA_PATH, str(chunk_id))
        create_dir(save_path)

        for file in files:
            filename = file.filename.split('/')[-1]

            # разрешим загрузку файлов пдф и изображений
            if not pp.check_extension(filename, FILE_EXTENSIONS | IMAGE_EXTENSIONS):
                warnings.warn("File extension is not supported.")
                continue

            file_path = os.path.join(save_path, filename)

            # сохраним файл в save_path
            with open(file_path, "wb") as wb_f:
                wb_f.write(file.file.read())
                paths.append(file_path)

            # если файл пдф, то конвертируем его в изображения
            if pp.check_extension(filename, FILE_EXTENSIONS):
                pdf_id = FilesManager.insert_data(FileStructure(
                    chunk_id=chunk_id,
                    old_filename=filename
                ))
                # выгрузим сканы в папку save_path
                i_save_path = os.path.join(save_path, str(pdf_id))
                create_dir(i_save_path)

                result = Data.pdf_to_images(file_path, i_save_path)
                paths += result

        return UploadFilesResponse(paths=paths)

    @staticmethod
    def get_folders(req: GetFRequest) -> GetFoldersResponse:
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

    @staticmethod
    def get_chunk_id() -> int:
        """Get the next chunk ID."""
        # Получение списка каталогов и фильтрация только числовых
        numeric_dirs = [dir_ for dir_ in os.listdir(DATA_PATH)
                        if dir_.isdigit() and os.path.isdir(os.path.join(DATA_PATH, dir_))]

        # Сортировка числовых каталогов и получение следующего ID
        if numeric_dirs:
            next_uid = max(map(int, numeric_dirs)) + 1
        else:
            next_uid = 1

        # Создание каталога для нового chunk ID
        create_dir(str(next_uid))
        return next_uid

    @staticmethod
    def archive_chunk(
            chunk_id: int,
            filename: str = "DATA") -> Optional[str]:
        """archive_chunk_service function service."""
        filename = unquote(filename)

        path = os.path.join(DATA_PATH, str(chunk_id))
        archive_path = os.path.join(DATA_PATH, str(chunk_id), filename + ".zip")

        if not os.path.exists(path):
            return None

        # getting data from DataBase and files from chunk_id dir
        datas = []
        for data in ProcessedManager.get_data_by_chunk_id(chunk_id):
            datas.append({
                "old_filename": data.old_filename,
                "new_filename": data.new_filename,
                "type": "image"
            })
        for data in FilesManager.get_data_by_chunk_id(chunk_id):
            datas.append({
                "old_filename": data.old_filename,
                "new_filename": data.new_filename,
                "type": "file"
            })

        # выделяем только файлы в папке chunk_id
        filenames = [
            i for i in os.listdir(path)
            if pp.check_extension(i, FILE_EXTENSIONS | IMAGE_EXTENSIONS)
        ]

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for data in datas:
                # if file is not in LOCAL_DATA/chunk_id/ dir
                if data["old_filename"] not in filenames:
                    continue
                old_path = os.path.join(DATA_PATH, str(chunk_id), data["old_filename"])

                if data["new_filename"] is None:
                    warnings.warn(f"No new filename for {old_path}.")
                    new_filename = data["old_filename"]
                else:
                    new_filename = data["new_filename"] + "." + data["old_filename"].split(".")[-1]

                if not os.path.exists(old_path):
                    warnings.warn(f"File {old_path} not found.")
                    continue

                zip_file.write(str(old_path), arcname=new_filename)

        return SERVER_PATH + os.path.join("LOCAL_DATA", str(chunk_id), filename + ".zip")
