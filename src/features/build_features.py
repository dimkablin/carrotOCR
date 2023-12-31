""" Image Processing Utilities

This module contains utility functions for image processing tasks.
You can see an example of usage in 'notebooks/preprocessing.ipynb'
"""
import io

from PIL import Image
import cv2
import numpy as np
from skimage.color import rgb2gray
from skimage.transform import (hough_line, hough_line_peaks)
from skimage.filters import threshold_otsu, sobel
from scipy.stats import mode
from scipy import ndimage

from src.api.models.process_image import Cut


def byte2numpy(image) -> np.ndarray:
    """ Read image bytes and return numpy array"""
    image = io.BytesIO(image)
    image = Image.open(image)
    image = pil2numpy(image)

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

    image = cv2.convertScaleAbs(
        image,
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


def binarize_image(rgb_image: np.ndarray) -> np.ndarray:
    """biniarize the image"""
    image = rgb2gray(rgb_image)
    threshold = threshold_otsu(image)
    bina_image = image < threshold
    return bina_image


def find_edges(bina_image: np.ndarray) -> np.ndarray:
    """sobel edge detection"""
    image_edges = sobel(bina_image)
    return image_edges


def find_tilt_angle(image_edges: np.ndarray) -> int:
    """find the tilt angle"""
    hspace, theta, distances = hough_line(image_edges)
    _, angles, _ = hough_line_peaks(hspace, theta, distances)
    angle = np.rad2deg(mode(angles, keepdims=True)[0][0])

    if abs(angle) == 45:
        angle = angle * 2

    if angle < 0:
        r_angle = angle + 90
    else:
        r_angle = 90

    return r_angle


def rotate_image(image: np.ndarray, angle: int) -> np.ndarray:
    """rotate the image"""
    # ndimage.rotate поворачивает картинку против часой стрелки поэтмоу минус
    image = ndimage.rotate(image, -angle)
    return image


def crop(image: np.ndarray,
         w2h_koeff: float) -> np.ndarray:
    """_summary_

    Args:
        image (np.ndarray): _description_
        width (_type_): _description_
        height (_type_): _description_
        w2h_koeff (_type_): _description_

    Returns:
        np.ndarray: _description_
    """
    height, width = image.shape[:2]
    if width > height:
        width = min(width, int(height*w2h_koeff))
    else:
        height = min(height, int(width/w2h_koeff))


    print(height, width)

    image = cut(
        image,
        Cut(x1=0, y1=0, height=height, width=width)
    )

    return image

def cut(image: np.ndarray, cut_: Cut) -> np.ndarray:
    """ Cut the image

    Args:
        image (np.ndarray): input
        cut (Cut): Base FastAPI Model

    Returns:
        np.ndarray: cuted image
    """

    return image[cut_.y1: cut_.y1 + cut_.height,
                 cut_.x1: cut_.x1 + cut_.width, :]
