"""MMOCR class Initialization."""
from typing import Any

from mmocr.apis import MMOCRInferencer

from src.models.ocr.ocr_interface import OCR
from src.utils.utils import get_abspath


class MMOCRInited(OCR):
    """ Initialized mmOCR model """

    def __init__(self):
        self.device = 'cpu'

        self.det = 'DBNet'
        self.det_weights = get_abspath('models/ocr/mmocr/dbnet/dbnet_resnet50-oclip.pth')

        self.rec = 'SAR'
        self.rec_config = get_abspath('models/ocr/mmocr/config.py')
        self.rec_weights = get_abspath('models/ocr/mmocr/sar/epoch_10.pth')

        self.model = MMOCRInferencer(det=self.det,
                                     det_weights=self.det_weights,
                                     rec=self.rec_config,
                                     rec_weights=self.rec_weights,
                                     device=self.device)

    def __call__(self, *args, **kwargs) -> list[dict[str, list[Any]]]:
        """ Using inference class to predict"""
        pred = self.model(*args, **kwargs)
        return pred['predictions']

    def __str__(self):
        """ Define the string representation of the MMOCR instance """
        return f"MMOCR(det={self.det}, rec={self.rec}, device={self.device})"

    @staticmethod
    def get_model_type() -> str:
        """Return model type."""
        return "mmocr"
