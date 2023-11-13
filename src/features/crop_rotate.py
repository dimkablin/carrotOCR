# pylint: disable=E
""" SOME DOCUMENTATION """

import numpy as np
from skimage.color import rgb2gray
from skimage.transform import (hough_line, hough_line_peaks)
from skimage.filters import threshold_otsu, sobel
from scipy.stats import mode
from scipy import ndimage


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
        r_angle = - 90 + 180

    return r_angle


def rotate_image(rgb_image: np.array, angle: int) -> np.array:
    """rotate the image"""
    fixed_image = ndimage.rotate(rgb_image, angle)
    return fixed_image


def cropped(img:str) -> np.array:
    """crop the image"""
    # img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
    h, w = img.shape[:2]
    if w >= h:
        img = img[0:h, 0:int(w/(0.7*(w/h)))]
    else:
        img = img[0:int(h/(0.7*(h/w))), 0:w]

    return img


def general_pipeline(img:np.array) -> np.array:
    """final processing of the image"""
    image = cropped(img)
    bina_image = binarize_image(image)
    image_edges = find_edges(bina_image)
    angle = find_tilt_angle(image_edges)
    return rotate_image(image, angle)
