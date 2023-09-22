""" mmOCR class initialization """
from mmocr.apis import MMOCRInferencer
from mmocr.apis.inferencers.base_mmocr_inferencer import InputsType
from models.ocr_interface import OCR


class MMOCRModel(OCR):
    """Class for mmOCR"""
    def __init__(self,
                 det: str = 'DBNet',
                 rec: str = 'SAR',
                 device: str = 'cpu',
                 **kwargs) -> None:
        """ Initialization of mmOCR inference class """
        self.det = det
        self.rec = rec
        self.device = device

        self.inference = MMOCRInferencer(det=self.det, rec=self.rec, device=self.device, **kwargs)

    def __call__(self, inputs: InputsType, *args, **kwargs) -> dict:
        """ Using inference class to predict"""
        pred = self.inference(inputs, **kwargs)
        return pred

    def __str__(self):
        """ Define the string representation of the MMOCR instance """
        return f"MMOCR(det={self.det}, rec={self.rec}, device={self.device})"
