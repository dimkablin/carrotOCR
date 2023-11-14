""" Image Processing Utilities

This module contains utility functions for image processing tasks.
You can see an example of usage in 'notebooks/preprocessing.ipynb'
"""
import asyncio
# pylint: disable=W,R,E

import io
from typing import List

from PIL import Image
import cv2
import numpy as np
from src.features.crop_rotate import general_pipeline

async def preprocess_image(image: np.ndarray) -> np.ndarray:
    """ Main function to preprocess image """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cut_image(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = adaptive_threshold(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    return image


async def preprocess_images(images: List[np.ndarray]) -> List[np.ndarray]:
    """ Main function to preprocess images """
    images = await asyncio.gather(*[preprocess_image(image) for image in images])
    return images


def byte2numpy(image) -> np.ndarray:
    """ Read image bytes and return numpy array"""
    image = io.BytesIO(image)
    image = Image.open(image)
    image = pil2numpy(image)

    return image


def cut_image(image: np.ndarray, k=1.4142, min_wh = 1200) -> np.ndarray:
    """ Changing size of the image from (w, h) to (new_w, k * new_w) where new_w equals to min(w, h)

    :param image: An Image.Image object representing input image
    :param k: A coefficient that shows how much longer the length is than the width
    :return: An Image.Image object
    """

    assert image.shape[2] == 3, \
        f"image shape has to be equal to (:, :, 3), but image.shape has {len(image.shape)}."
    height, width = image.shape[0], image.shape[1]
    height = int(min(k * width, height))

    height = height if height > min_wh else min_wh
    width = width if width > min_wh else min_wh

    image = image[0:width, 0:height, :]

    return image


def check_exif(image: Image.Image) -> Image.Image:
    """ Checking exif attribute

    :param image: An Image.Image object
    :return: An Image.Image rotated object according to the attribute
    """
    if hasattr(image, '_getexif') and image._getexif() is not None:
        exif = dict(image._getexif().items())

        if exif.get(274) == 3:
            image = image.rotate(180, expand=True)
        elif exif.get(274) == 6:
            image = image.rotate(270, expand=True)
        elif exif.get(274) == 8:
            image = image.rotate(90, expand=True)

    return image


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


async def pipeline_async(images, paths):
    """
    crop and rotate list of images
    """
    return [await general_pipeline(image, path) for image, path in zip(images, paths)]


def pil2numpy(image: Image.Image) -> np.ndarray:
    """ Convert a PIL image to a NumPy array.

    :param image: An Image.Image object representing the input image.
    :return: A NumPy array representing the image.
    """

    return np.array(image, dtype=np.uint8)


def blur(image: np.ndarray,
         kernel: tuple[int, int] = (3, 3),
         sigma: int = 3) -> np.ndarray:
    """ Apply Gaussian blur to the input image.

    :param image: The input image as a NumPy array.
    :param kernel: A tuple specifying the size of the Gaussian blur kernel (width, height).
    :param sigma: The standard deviation of the Gaussian blur.
        Higher values result in stronger blur.
    :return: The blurred image as a NumPy array.
    """

    image = cv2.GaussianBlur(image, kernel, sigma)
    return image


def denoising(image: np.ndarray,
              kernel: np.ndarray = np.ones((3, 3), np.uint8),
              iterations: int = 1) -> np.ndarray:
    """ Apply denoising to the input image.

    :param image: A NumPy array representing the input image.
    :param kernel: A NumPy array representing the kernel for erosion and dilation operations.
        By default, it's a 2x2 matrix with data type np.uint8.
    :param iterations: The number of times the erosion and dilation operations are applied.
    :return: A NumPy array representing the denoised image.
    """

    image = cv2.erode(image, kernel, iterations=iterations)
    image = cv2.dilate(image, kernel, iterations=iterations)
    return image


def clahe(image: np.ndarray,
          clip_limit: int = 2,
          tile_grid_size: tuple[int, int] = (8, 8)) -> np.ndarray:
    """ Apply clahe histogram equalization

    :param image: The input image (grayscale).
    :param clip_limit: The contrast limit for CLAHE.
    :param tile_grid_size: The size of the grid for histogram equalization. Default is (8, 8).
    :return: The contrast-enhanced image.
    """

    clahe_ = cv2.createCLAHE(clip_limit, tile_grid_size)
    image = clahe_.apply(image)

    return image


def threshold(image: np.ndarray,
              thresh: int = 220,
              maxval: int = 255,
              threshold_type: int = cv2.THRESH_BINARY) -> np.ndarray:
    """ Apply thresholding to the input image.

    :param image: A NumPy array representing the input image.
    :param thresh: The threshold value used for binarization. Pixels below this value become 0.
    :param maxval: The maximum value assigned to pixels that exceed the threshold.
    :param threshold_type: The thresholding type
    :return: A NumPy array representing the thresholded image.
    """

    _, image = cv2.threshold(image, thresh, maxval, threshold_type)
    return image


def adaptive_threshold(image: np.ndarray,
                       maxval: int = 255,
                       adaptive_method: int = cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                       threshold_type: int = cv2.THRESH_BINARY,
                       block_size: int = 501,
                       c_var: float = 45) -> np.ndarray:
    """ Apply adaptive thresholding to the input image.

    :param image: A NumPy array representing the input image.
    :param maxval: The maximum pixel value used for thresholding.
    :param adaptive_method: The adaptive thresholding method to use
        (e.g., cv2.ADAPTIVE_THRESH_GAUSSIAN_C).
    :param threshold_type: The type of thresholding (e.g., cv2.THRESH_BINARY).
    :param block_size: The blockSize determines the size of the neighbourhood area
    :param c_var: C is a constant that is subtracted from the mean or weighted
        sum of the neighbourhood pixels.

    :return: A NumPy array representing the thresholded image.
    """

    image = cv2.adaptiveThreshold(image,
                                  maxval,
                                  adaptive_method,
                                  threshold_type,
                                  block_size,
                                  c_var)
    return image


def contrast_enhancement(image: np.ndarray) -> np.ndarray:
    """ Enhance the contrast of the input image.

    :param image: A NumPy array representing the input image.
    :return: A NumPy array representing the contrast-enhanced image.
    """

    min_val, max_val, _, _ = cv2.minMaxLoc(image)
    image = cv2.convertScaleAbs(image,
                                alpha=255.0 / (max_val - min_val),
                                beta=-min_val * (255.0 / (max_val - min_val))
                                )

    return image


def sobel_filter(image: np.ndarray,
                 ksize: int = 3) -> np.ndarray:
    """ Apply Sobel filter to the input image

    :param image: A NumPy array representing the input image
    :param ksize: The kernel size of sobel filter
    :return: A NumPy array representing edge-enhanced image
    """

    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize)
    image = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    return image


def invert(image: np.ndarray) -> np.ndarray:
    """ Invert thr colors of the input image

    :param image: A NumPy array representing the input image.
    :return: A NumPy array representing the inverted image.
    """

    image = cv2.bitwise_not(image)
    return image


def blend(image1: np.ndarray,
          image2: np.ndarray,
          alpha: float = 0.5) -> np.ndarray:
    """ Averaging two images with a coefficient 1-alpha and alpha

    :param image1: The first image
    :param image2: The second image
    :param alpha: The coefficient that has to be between 0 and 1
    :return: A np.ndarray object representing the average image
    """

    image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
    return image
