# pylint: disable=E
""" SOME DOCUMENTATION """

from typing import Optional

import cv2
import numpy as np
from src.api.models.process_chunk import ProgressResponse
from src.api.models.process_image import Cut, PipelineParams
from src.api.routers.utils import send_progress_sync
from src.features import build_features as pp

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
        path (str): path to save result image
        pipeline_params (Optional[PipelineParams], optional): Pipeline args. Defaults to None.

    Returns:
        np.ndarray: The image after pipeline
    """

    # set config for pipeline
    if pipeline_params is None:
        w2h_koeff = 0 if ( 0.4 < image.shape[0]/image.shape[1] < 2.5 ) else 1
        pipeline_params = PipelineParams(
            angle=0,
            w2h_koeff=w2h_koeff,
            cut=Cut(x1=0, y1=0, height=image.shape[0], width=image.shape[1])
        )

    if pipeline_params.w2h_koeff > 0:
        image = pp.crop(image, pipeline_params.w2h_koeff)

    if pipeline_params.cut.width !=0 and pipeline_params.cut.height != 0:
        image = pp.cut(image, pipeline_params.cut)

    # prepare images by pipeline config (rotate and cut)
    image = pp.rotate_image(image, pipeline_params.angle)

    return image


def pipeline_images(images, connections=None):
    """
    crop and rotate list of images
    """
    result = []
    for i, image in enumerate(images):
        result.append(pipeline_image(image))

        # send progress via connection
        if connections is not None:
            for connection in connections:
                send_progress_sync(
                    connection,
                    ProgressResponse(
                        iter=i,
                        length=2 * len(images),
                        message="Предобработка данных."
                    )
                )

    return result
