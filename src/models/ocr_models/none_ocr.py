"""Trained EasyOCR Initialization."""
from typing import Any
from src.models.ocr_models.ocr_interface import OCR


class NoneOCRInited(OCR):
    """ Initialized EasyOCR model """

    def __call__(self, *args, **kwargs) -> list[dict[str, list[Any]]]:
        """Return empty ocr like results"""
        results = [
            {'rec_texts': [], 'rec_scores': [], 'det_polygons': [], 'det_scores': []}
        ]

        return results

    def __str__(self):
        return "Return empty ocr like results"

    @staticmethod
    def get_model_type() -> str:
        """Return model type."""
        return "None"
