""" Factory Method - Design Pattern """
from src.ai_models.ocr_models.easyocr import EasyOCRInited
from src.ai_models.ocr_models.easyocr_custom import EasyOCRInitedCustom
from src.ai_models.ocr_models.pytesseract import PyTesseractInited
from src.ai_models.ocr_models.none_ocr import NoneOCRInited


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        NoneOCRInited.get_model_type(): NoneOCRInited(),
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
        """ Getter of ai_models name """
        return OCRModelFactory.MODEL_MAPPING.keys()