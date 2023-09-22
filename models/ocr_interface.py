""" The ocr interface """

from abc import ABC, abstractmethod


class OCR(ABC):
    """ Interface of ocr models """
    @abstractmethod
    def __call__(self, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
