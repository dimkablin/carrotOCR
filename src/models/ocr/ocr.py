""" Factory Method - Design Pattern """
from src.models.ocr.easyocr import EasyOCRInited
from src.models.ocr.easyocr import EasyOCRInitedCustom
from src.models.ocr.pytesseract import PyTesseractInited


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        PyTesseractInited.get_model_type(): PyTesseractInited(),
        EasyOCRInited.get_model_type(): EasyOCRInited(),
        EasyOCRInitedCustom.get_model_type(): EasyOCRInitedCustom(),
    }

    @staticmethod
    def get(model_type):
        """ Create OCR model by its name """
        model = OCRModelFactory.MODEL_MAPPING.get(model_type)

        if model is None:
            raise ValueError("Invalid OCR model type")
        return model

    @staticmethod
    def get_models():
        """ Getter of models name """
        return OCRModelFactory.MODEL_MAPPING.keys()
