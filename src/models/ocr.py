""" Factory Method - Design Pattern """
from typing import Any

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

    def __call__(self, *args, **kwargs) -> list[dict[str, list[Any]]]:
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
        self.psm = 6
        self.config = f"--oem {self.oem} --psm {self.psm} --tessdata-dir {self.local_config_dir}"
        self.thresh = 0.3

    def __call__(self, inputs, *args, **kwargs) -> list[dict[str, list[Any]]]:
        results = []
        for image in inputs:
            outputs = pytesseract.image_to_data(image,
                                                lang='tat',
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
                # if rec is empty or it's lower than thresh
                if conf == -1 or conf/100. < self.thresh:
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

            results.append(result)

        return results

    def __str__(self):
        return f"PyTesseract OCR --oem {self.oem} --psm {self.psm}"


class EasyOCRInited(OCR):
    """ Initialized EasyOCR model """
    def __init__(self):
        self.languages = ['ru']
        self.use_cuda = False
        self.model = easyocr.Reader(self.languages,
                                    gpu=self.use_cuda,
                                    recog_network='cyrillic_g2')

    def __call__(self, inputs, *args, **kwargs) -> list[dict[str, list[Any]]]:
        results = []
        for image in inputs:
            horizontal_boxes, free_boxes = self.model.detect(image)
            outputs = self.model.recognize(image, horizontal_boxes[0], free_boxes[0])

            result = {
                'rec_texts': [],
                'rec_scores': [],
                'det_polygons': [],
                'det_scores': []
            }

            for bbox, text, conf in outputs:
                result['det_scores'].append(1)
                result['det_polygons'].append([coord for xy in bbox for coord in xy])
                result['rec_scores'].append(conf)
                result['rec_texts'].append(text)
            results.append(result)

        return results

    def __str__(self):
        return f"EasyOCR lang {self.languages}"


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
