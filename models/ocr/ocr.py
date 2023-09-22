""" Factory Method - Design Pattern """
from models.ocr.mmocr.model import MMOCRModel


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        "mmocr": MMOCRModel,
        "pytesseract": None,
        "easyocr": None,
    }

    @staticmethod
    def create(model_type):
        """ Create OCR model by its name """
        model_class = OCRModelFactory.MODEL_MAPPING.get(model_type)

        if model_class is None:
            raise ValueError("Invalid OCR model type")
        return model_class

    @staticmethod
    def __str__() -> str:
        return str(OCRModelFactory.MODEL_MAPPING.keys())

    @staticmethod
    def __len__() -> int:
        return len(OCRModelFactory.MODEL_MAPPING)
