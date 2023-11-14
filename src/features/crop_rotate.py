# pylint: disable=E
""" SOME DOCUMENTATION """
import numpy as np
from skimage.color import rgb2gray
from skimage.transform import (hough_line, hough_line_peaks)
from skimage.filters import threshold_otsu, sobel
from scipy.stats import mode
from scipy import ndimage
from src.utils.utils import save_image


def binarize_image(rgb_image: np.array) -> np.array:
    """biniarize the image"""
    image = rgb2gray(rgb_image)
    threshold = threshold_otsu(image)
    bina_image = image < threshold
    return bina_image


def find_edges(bina_image: np.array) -> np.array:
    """sobel edge detection"""
    image_edges = sobel(bina_image)
    return image_edges


def find_tilt_angle(image_edges: np.array) -> int:
    """find the tilt angle"""
    h, theta, d = hough_line(image_edges)
    _, angles, _ = hough_line_peaks(h, theta, d)
    angle = np.rad2deg(mode(angles, keepdims=True)[0][0])

    if abs(angle) == 45:
        angle = angle * 2

    if angle < 0:
        r_angle = angle + 90
    else:
        r_angle = 90

    return r_angle


def rotate_image(rgb_image: np.array, angle: int) -> np.array:
    """rotate the image"""
    fixed_image = ndimage.rotate(rgb_image, angle)
    return fixed_image


def cropped(img:str) -> np.array:
    """crop the image"""
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


async def pipeline_image(img:np.array, path:str, angle:int=None) -> np.array:
    """final processing of the image"""
    image = cropped(img)
    save_image(path, image)
    bina_image = binarize_image(image)
    image_edges = find_edges(bina_image)

    if angle is None:
        angle = find_tilt_angle(image_edges)
    image = rotate_image(image, angle)
    return image
