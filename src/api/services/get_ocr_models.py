"""Get OCR Models service."""
from src.api.models.get_ocr_models import GetOCRModelsResponse
from src.models.ocr import OCRModelFactory


def get_ocr_models_service() -> GetOCRModelsResponse:
    """Get OCR Models service function."""
    models = OCRModelFactory.get_models()
    return GetOCRModelsResponse(models=models)
