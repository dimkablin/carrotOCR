""" The ocr interface """

from abc import ABC, abstractmethod


class OCR(ABC):
    """ Interface of ocr models """
    @abstractmethod
    def __call__(self, *args, **kwargs) -> dict:
        """
        Perform OCR on an image.

        Returns:
            dict: A dictionary containing the OCR result.
                  - 'bbox': tuple representing bounding box coordinates
                  - 'text': string representing the recognized text
        """

    @abstractmethod
    def __str__(self) -> str:
        pass
