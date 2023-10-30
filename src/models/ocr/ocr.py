""" Factory Method - Design Pattern """
from src.models.ocr.easyocr import EasyOCRInited
from src.models.ocr.easyocr import EasyOCRInitedCustom
from src.models.ocr.pytesseract import PyTesseractInited


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        PyTesseractInited.get_model_type(): PyTesseractInited,
        EasyOCRInited.get_model_type(): EasyOCRInited,
        EasyOCRInitedCustom.get_model_type(): EasyOCRInitedCustom,
    }

    @staticmethod
    def create(model_type):
        """ Create OCR model by its name """
        model_class = OCRModelFactory.MODEL_MAPPING.get(model_type)

        if model_class is None:
            raise ValueError("Invalid OCR model type")
        return model_class()

    @staticmethod
    def get_models():
        """ Getter of models name """
        return OCRModelFactory.MODEL_MAPPING.keys()


class OCRModelFactoryProcessor:
    """OCR Model Processor."""
    def __init__(self, model_type):
        self.model = OCRModelFactory.create(model_type)

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

    def change_ocr_model(self, model_type: str):
        """Change OCR model function"""
        del self.model
        self.model = OCRModelFactory.create(model_type)

    def get_current_model(self) -> str:
        """Return the current running model."""
        return self.model.get_model_type()
