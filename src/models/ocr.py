""" Factory Method - Design Pattern """

from models.mmocr.model import MMOCRModel


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
        return model_class()

    def __str__(self) -> str:
        return str(OCRModelFactory.MODEL_MAPPING.keys())

    def __len__(self) -> int:
        return len(OCRModelFactory.MODEL_MAPPING)
