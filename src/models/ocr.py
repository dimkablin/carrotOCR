""" Factory Method - Design Pattern """
from src.models.ocr_models.easyocr import EasyOCRInited
from src.models.ocr_models.easyocr_custom import EasyOCRInitedCustom
from src.models.ocr_models.pytesseract import PyTesseractInited
from src.models.ocr_models.none_ocr import NoneOCRInited


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        PyTesseractInited.get_model_type(): PyTesseractInited(),
        EasyOCRInited.get_model_type(): EasyOCRInited(),
        EasyOCRInitedCustom.get_model_type(): EasyOCRInitedCustom(),
        NoneOCRInited.get_model_type(): NoneOCRInited(),
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
