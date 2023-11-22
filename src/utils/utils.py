# pylint: disable=E
""" Functions to work with environment """

import os
from typing import List

import cv2
import numpy as np

from src.api.models.get_processed import TBox
from src.env import project_dir


def get_abspath(*path):
    """ Get the absolute path from this file and add the argument path"""
    return os.path.join(project_dir, *path)


def read_paths(dir_: str) -> List[str]:
    """Return the paths from the dir"""
    return [get_abspath(dir_, f) for f in os.listdir(dir_)]


def bbox2rect(bbox: List[int]) -> TBox:
    """Convert from 4 points represent a model output's bbox to Point Width High."""
    min_xy = (min(bbox[::2]),min(bbox[1::2]))
    max_xy = (max(bbox[::2]),max(bbox[1::2]))

    result = TBox(
        x=min_xy[0],
        y=min_xy[1],
        w=max_xy[0]-min_xy[0],
        h=max_xy[1]-min_xy[1]
    )
    return result


def bboxes2rect(bboxes: List[List[int]]) -> List[TBox]:
    """Convert list of bboxes to rectangles."""
    result = []
    for bbox in bboxes:
        result.append(bbox2rect(bbox))

    return result


def create_dir_if_not_exist(path_: str) -> None:
    """Creating directory if it doesn't exist."""
    if not os.path.exists(path_):
        os.mkdir(path_)


def save_image(image_path: str, image: np.ndarray) -> None:
    """Save an image."""

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_path, image)

def save_images(images: List[np.ndarray], image_names: List[str], path: str) -> None:
    """Save images to path/names[i]"""
    create_dir_if_not_exist(path)

    for i, image in enumerate(images):
        save_image(path + "/" + image_names[i], image)
