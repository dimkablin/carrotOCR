"""Crud of functions for database"""
from typing import List, Any

from src.db.processed_manager import ProcessedManager
from src.db.files_manager import FilesManager

from src.utils.utils import bboxes2rect
from src.api.models.database import *


class Database:
    """Crud of functions for database"""
    @staticmethod
    def get_processed(req: GetProcessedRequest) -> GetProcessedResponse:
        """get_processed service's main function ."""

        data = ProcessedManager.get_data_by_id(req.uid)
        result = GetProcessedResponse(
            chunk_id=data.chunk_id,
            angle=data.angle,
            old_filename=data.old_filename,
            new_filename=data.new_filename,
            tags=data.tags,
            text=data.text,
            bboxes=bboxes2rect(data.bboxes)
        )
        return result

    @staticmethod
    def add_filenames(req: AddFilenameRequest):
        """Adding new filenames service."""
        if req.is_duplicate:
            return False

        if req.file_type == "image":
            return ProcessedManager.insert_new_filename(req.filename, req.uid)
        elif req.file_type == "file":
            return FilesManager.insert_new_filename(req.filename, req.uid)

        return False

    @staticmethod
    def get_data_by_chunk_id(chunk_id: int) -> List[Any]:
        """Return data by chunk id"""
        return ProcessedManager.get_data_by_chunk_id(chunk_id)

    @staticmethod
    def delete_data_by_id_chunk(chunk_id: int) -> bool:
        """ Clear data by chunk id"""
        return ProcessedManager().delete_data_by_chunk_id(chunk_id)

    @staticmethod
    def delete_data_by_id(uid: int) -> bool:
        """Delete data from the database by id."""
        return ProcessedManager.delete_data_by_id(uid)
