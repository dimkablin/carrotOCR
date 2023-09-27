""" Factory Method - Design Pattern """

# mmOCR
from mmocr.apis import MMOCRInferencer
from pytesseract import Output
import pytesseract
import easyocr

from src.utils.utils import get_abspath
from src.models.ocr_interface import OCR


class MMOCRInited(OCR):
    """ Initialized mmOCR model """
    def __init__(self):
        self.det = 'DBNet'
        self.det_weights = get_abspath('models/ocr/mmocr/dbnet/dbnet_resnet50-oclip.pth')

        self.rec = 'SAR'
        self.rec_config = get_abspath('models/ocr/mmocr/config.py')
        self.rec_weights = get_abspath('models/ocr/mmocr/sar/epoch_10.pth')

        self.device = 'cpu'

        self.model = MMOCRInferencer(det=self.det,
                                     det_weights=self.det_weights,
                                     rec=self.rec_config,
                                     rec_weights=self.rec_weights,
                                     device=self.device)

    def __call__(self, *args, **kwargs) -> dict:
        """ Using inference class to predict"""
        pred = self.model(*args, **kwargs)
        return pred['predictions']

    def __str__(self):
        """ Define the string representation of the MMOCR instance """
        return f"MMOCR(det={self.det}, rec={self.rec}, device={self.device})"


class PyTesseractInited(OCR):
    """ Initialized PyTesseract model """
    def __init__(self):
        self.local_config_dir = 'models/ocr/pytesseract'
        self.oem = 3
        self.psm = 3
        self.config = f"--oem {self.oem} --psm {self.psm} --tessdata-dir {self.local_config_dir}"

    def __call__(self, inputs, *args, **kwargs) -> dict:
        outputs = pytesseract.image_to_data(inputs,
                                         lang='rus',
                                         config=self.config,
                                         output_type=Output.DICT,
                                         *args,
                                         **kwargs)
        result = {
            'rec_texts': [],
            'rec_scores': [],
            'det_polygons': [],
            'det_scores': []
        }

        for i, conf in enumerate(outputs['conf']):
            # if rec is empty
            if conf == -1:
                continue

            x_bbox = outputs['left'][i]
            y_bbox = outputs['top'][i]
            width = outputs['width'][i]
            height = outputs['height'][i]

            result['det_scores'].append(1)
            result['det_polygons'].append([x_bbox, y_bbox,
                                           x_bbox + width, y_bbox,
                                           x_bbox + width, y_bbox + height,
                                           x_bbox, y_bbox + height])
            result['rec_scores'].append(conf / 100.)
            result['rec_texts'].append(outputs['text'][i])

        return result

    def __str__(self):
        return f"PyTesseract OCR --oem {self.oem} --psm {self.psm}"


class EasyOCRInited(OCR):
    """ Initialized EasyOCR model """
    def __init__(self):
        self.model = easyocr.easyocr.detection_models

    def __call__(self, *args, **kwargs) -> dict:
        pass

    def __str__(self):
        return "EasyOCR"


class OCRModelFactory:
    """ Factory Method - Design Pattern implementation """

    MODEL_MAPPING = {
        "mmocr": MMOCRInited,
        "pytesseract": PyTesseractInited,
        "easyocr": EasyOCRInited,
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
