""" Factory Method - Design Pattern """
from src.models.ocr.easyocr import EasyOCRInited
from src.models.ocr.mmocr import MMOCRInited
from src.models.ocr.pytesseract import PyTesseractInited


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        MMOCRInited.get_model_type(): MMOCRInited,
        PyTesseractInited.get_model_type(): PyTesseractInited,
        EasyOCRInited.get_model_type(): EasyOCRInited,
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