""" Functions to work with environment """

import os
from typing import List

import cv2
import numpy as np

from src.env import project_dir


def get_abspath(path):
    """ Get the absolute path from this file and add the argument path"""
    return os.path.join(project_dir, path)


def bbox2rect(bbox: List[int]) -> List[int]:
    """Convert from 4 points represent a model output's bbox to Point Width High."""
    (center_x, center_y), (width, height), angle = cv2.minAreaRect(np.array(bbox).reshape(-1, 2))
    result = [
        center_x - width//2,
        center_y - height//2,
        width,
        height
    ]
    return result


def bboxes2rect(bboxes: List[List[int]]) -> List[List[int]]:
    """Convert list of bboxes to rectangles."""
    result = []
    for bbox in bboxes:
        result.append(bbox2rect(bbox))

    return result
