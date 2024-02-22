"""Pytesseract OCR Initialization."""
import easyocr
import pytesseract
from typing import Any
from src.env import USE_CUDA
from pytesseract import Output
from src.ai_models.ocr_models.ocr_interface import OCR
from src.features.extract_features import read_image

class PyTesseractCraftTrained(OCR):
    """ Initialized PyTesseract model """
    def __init__(self, psm=13):
        self.local_config_dir = 'src/ai_models/weights/ocr/pytesseract'
        self.psm = psm
        self.oem = 1
        self.config = f"--oem {self.oem} --psm {self.psm} --tessdata-dir {self.local_config_dir}"
        self.thresh = 0.3

        #FOR DETECTOR. EasyOCR uses the craft detector
        self.languages = ['ru']
        self.use_cuda = USE_CUDA
        self.detector = easyocr.Reader(
            self.languages,
            gpu=self.use_cuda,
            model_storage_directory='src/ai_models/weights/ocr/easyocr/model',
            user_network_directory='src/ai_models/weights/ocr/easyocr/user_network',
            download_enabled=False,
            recog_network='cyrillic_g2'
        )

    def __call__(self, inputs, *args, **kwargs) -> list[dict[str, list[Any]]]:

        results = []
        for image in inputs:

            result = {'rec_texts': [], 'rec_scores': [], 'det_polygons': [], 'det_scores': []}

            bboxes = self.detector.detect(image)
            for box in bboxes[0][0]:
                x_min, x_max, y_min, y_max = box
                cropped_image = image[y_min:y_max, x_min:x_max]

                output = pytesseract.image_to_string(cropped_image, lang='rus2', config=self.config).strip()
                result['det_scores'].append(1)
                result['det_polygons'].append([int(x_min), int(y_min),
                                               int(x_max), int(y_min),
                                               int(x_max), int(y_max),
                                               int(x_min), int(y_max)])
                result['rec_scores'].append(1)
                result['rec_texts'].append(str(output))
            results.append(result)
            
        return results

    def __str__(self):
        return f"PyTesseract OCR --oem {self.oem} --psm {self.psm}"

    @staticmethod
    def get_model_type() -> str:
        """Return model type."""
        return "Craft Tesseract"
