# pylint: disable=E
""" SOME DOCUMENTATION """

import asyncio
from typing import Optional

import cv2
import numpy as np
from src.api.models.process_image import PipelineParams
from src.features.build_features import binarize_image, find_edges, find_tilt_angle, rotate_image
from src.utils.utils import save_image


async def read_image(path: str):
    """ Async open an image

    :param path: A string object representing the path to the image file
    :return: An Image.Image object representing the output image.
    """

    return await asyncio.to_thread(cv2.imread, path)


async def read_images(paths):
    """ Async read all images

    :param paths:
    :return:
    """
    return await asyncio.gather(*[read_image(path) for path in paths])


def _pipeline_image(
        image: np.ndarray,
        pipeline_params: PipelineParams) -> np.ndarray:
    """Preprocess image"""
    
    image = rotate_image(image, pipeline_params.angle)
    return image


async def pipeline_image(
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
        image = cropped(image)
        bina_image = binarize_image(image)
        image_edges = find_edges(bina_image)
        angle = find_tilt_angle(image_edges)

        pipeline_params = PipelineParams(
            angle=angle,
            w2h_koeff=1,
            area_to_process=None
        )

    _pipeline_image(image, pipeline_params)
    save_image(path, image)
    return image


async def pipeline_images(images, paths):
    """
    crop and rotate list of images
    """
    return await asyncio.gather(
        *[pipeline_image(image, path) for image, path in zip(images, paths)]
    )


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
