""" Factory Method - Design Pattern """

from mmocr.apis import MMOCRInferencer
from src.utils.utils import get_abspath
from src.models.ocr_interface import OCR


class MMOCRModelInited(OCR):
    """ Initialized mmOCR model """
    def __init__(self):
        self.det = 'DBNet'
        self.det_weights = get_abspath(r'models\ocr\mmocr\dbnet\dbnet_resnet50-oclip.pth')

        self.rec = 'SAR'
        self.rec_config = get_abspath(r'models\ocr\mmocr\config.py')
        self.rec_weights = get_abspath(r'models\ocr\mmocr\sar\epoch_10.pth')

        self.device = 'cuda'

        self.model = MMOCRInferencer(det=self.det,
                                     det_weights=self.det_weights,
                                     rec=self.rec_config,
                                     rec_weights=self.rec_weights,
                                     device=self.device)

    def __call__(self, *args, **kwargs) -> dict:
        """ Using inference class to predict"""
        pred = self.model(*args, **kwargs)
        return pred

    def __str__(self):
        """ Define the string representation of the MMOCR instance """
        return f"MMOCR(det={self.det}, rec={self.rec}, device={self.device})"


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        "mmocr": MMOCRModelInited,
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

    @staticmethod
    def get_models():
        """ Getter of models name """
        return OCRModelFactory.MODEL_MAPPING.keys()
