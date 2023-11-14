import numpy as np
import cv2
from skimage.color import rgb2gray
from skimage.transform import (hough_line, hough_line_peaks)
from scipy.stats import mode
from scipy import ndimage
from skimage import io
from skimage.filters import threshold_otsu, sobel
import matplotlib.pyplot as plt


def binarizeImage(RGB_image:np.array) -> np.array:
    """biniarize the image"""
    image = rgb2gray(RGB_image)
    threshold = threshold_otsu(image)
    bina_image = image < threshold
    return bina_image


def findEdges(bina_image:np.array) -> np.array:
    """sobel edge detection"""
    image_edges = sobel(bina_image)
    return image_edges


def findTiltAngle(image_edges:np.array) -> int:
    """find the tilt angle"""
    h, theta, d = hough_line(image_edges)
    accum, angles, dists = hough_line_peaks(h, theta, d)
    angle = np.rad2deg(mode(angles, keepdims=True)[0][0])
    
    if abs(angle)==45: angle = angle*2

    if (angle < 0):
        r_angle = angle + 90
    else:
        r_angle = - 90 + 180
 
    return r_angle


def rotateImage(RGB_image:np.array, angle:int) -> np.array:
    """rotate the image"""
    fixed_image = ndimage.rotate(RGB_image, angle)
    return fixed_image


def cropped(img:str) -> np.array:
    """crop the image"""
    # img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
    h, w = img.shape[:2]

    if w >= h:
        if w > 5000: img = img[0:h, 0:h] 
        # img = img[0:h, 0:int(w/(0.75*(w/h)))] 
    else:
        if h > 1920: img = img[0:w, 0:w]
        # img = img[0:int(h/(0.75*(h/w))), 0:w]

    return img


def generalPipeline(img:np.array) -> (np.array, np.array):
    """final processing of the image"""
    image = cropped(img)
    base_image = image.copy()
    bina_image = binarizeImage(image)
    image_edges = findEdges(bina_image)
    angle = findTiltAngle(image_edges)
    return rotateImage(image, angle)