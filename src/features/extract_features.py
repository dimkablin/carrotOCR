# pylint: disable=E
""" SOME DOCUMENTATION """

from typing import Optional

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from src.api.models.ai_models import Cut, PipelineParams
from src.features import build_features as bf


def check_extension(filename, extensions) -> bool:
    """Check available filename extension"""
    ext = filename.split(".")[-1]
    return ext.lower() in extensions


def read_image(path: str):
    """ Async open an image

    :param path: A string object representing the path to the image file
    :return: An Image.Image object representing the output image.
    """
    image = cv2.imread(path)
    return image


def read_images(paths):
    """ Async read all images

    :param paths:
    :return:
    """
    return [read_image(path) for path in paths]


def pipeline_image(
        image: np.ndarray,
        pipeline_params: Optional[PipelineParams] = None) -> np.ndarray:
    """ final processing of the image

    Args:
        image (np.ndarray): input image
        pipeline_params (Optional[PipelineParams], optional): Pipeline args. Defaults to None.

    Returns:
        np.ndarray: The image after pipeline
    """

    # set config for pipeline
    if pipeline_params is None:
        w2h_koeff = 0 if (0.4 < image.shape[0]/image.shape[1] < 2.5) else 1
        pipeline_params = PipelineParams(
            angle=0,
            w2h_koeff=w2h_koeff,
            cut=Cut(x1=0, y1=0, height=image.shape[0], width=image.shape[1])
        )

    if pipeline_params.w2h_koeff > 0:
        image = bf.crop(image, pipeline_params.w2h_koeff)

    if pipeline_params.cut.width != 0 and pipeline_params.cut.height != 0:
        image = bf.cut(image, pipeline_params.cut)

    # prepare images by pipeline config (rotate and cut)
    image = bf.rotate_image(image, pipeline_params.angle)

    return image


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Preprocess the input image"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.filter2D(image, -1, np.ones((3, 1), np.float32) / 3)
    image = bf.stretch_image(image, k=1.5)
    image = bf.normalize_image(image, mean=0.5)

    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    return image


def count_files(directory_path):
    """
    Counts the number of files in a dir
    :param directory_path:
    :return:
    """
    file_count = 0

    for root, dirs, files in os.walk(directory_path):
        file_count += len(files)

    return file_count
