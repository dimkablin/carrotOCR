# pylint: disable=E
""" Functions to work with environment """

import os
from typing import List

from src.api.models.database import TBox
from src.env import project_dir, DATA_PATH


def get_abspath(*path):
    """ Get the absolute path from this file and add the argument path"""
    return os.path.join(project_dir, *path)


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


def create_dir(dirname: str = None) -> None:
    """create_chunk_id_dir function service."""
    path = os.path.join(DATA_PATH, dirname) if dirname else DATA_PATH

    if not os.path.exists(path):
        os.mkdir(path)
