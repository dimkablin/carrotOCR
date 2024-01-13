# pylint: disable=E
""" SOME DOCUMENTATION """

from typing import Optional

import cv2
import numpy as np
from src.api.models.process_chunk import ProgressResponse
from src.api.models.process_image import Cut, PipelineParams
from src.api.services.process_chunk import send_progress_sync
from src.features import build_features as pp
from src.utils.utils import save_image


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


def _pipeline_image(
        image: np.ndarray,
        pipeline_params: PipelineParams) -> np.ndarray:
    """Preprocess image"""

    image = pp.rotate_image(image, pipeline_params.angle)

    if pipeline_params.w2h_koeff > 0:
        image = pp.crop(image, pipeline_params.w2h_koeff)
    else:
        image = pp.cut(image, pipeline_params.cut)

    return image


def pipeline_image(
        image: np.ndarray,
        path: str,
        pipeline_params: Optional[PipelineParams] = None) -> np.ndarray:
    """ final processing of the image

    Args:
        image (np.ndarray): input image
        path (str): path to save result image
        pipeline_params (Optional[PipelineParams], optional): Pipeline args. Defaults to None.

    Returns:
        np.ndarray: The image after pipeline
    """

    if pipeline_params is None:
        w2h_koeff = 0 if ( 0.4 < image.shape[0]/image.shape[1] < 2.5 ) else 1
        pipeline_params = PipelineParams(
            angle=0,
            w2h_koeff=w2h_koeff,
            cut=Cut(x1=0, y1=0, height=image.shape[0], width=image.shape[1])
        )

    save_image(path, image)
    image = _pipeline_image(image, pipeline_params)

    return image


def pipeline_images(images, paths, connections=None):
    """
    crop and rotate list of images
    """
    result = []
    for i, (image, path) in enumerate(zip(images, paths)):
        result.append(pipeline_image(image, path))

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


def cropped(img: np.ndarray) -> np.ndarray:
    """Cropping the image 

    Args:
        img (np.ndarray): input image

    Returns:
        np.ndarray: cropped image
    """
    # img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
    height, width = img.shape[:2]

    if width >= height:
        if width > 5000:
            img = img[0:height, 0:height]
        # img = img[0:h, 0:int(w/(0.75*(w/h)))]
    else:
        if height > 1920:
            img = img[0:width, 0:width]
        # img = img[0:int(h/(0.75*(h/w))), 0:w]
    return img
