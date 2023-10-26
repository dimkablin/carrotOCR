"""Pytesseract OCR Initialization."""
from typing import Any
from pytesseract import Output
import pytesseract
from src.models.ocr.ocr_interface import OCR


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
            result = {'rec_texts': [], 'rec_scores': [], 'det_polygons': [], 'det_scores': []}

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

    @staticmethod
    def get_model_type() -> str:
        """Return model type."""
        return "pytesseract"
