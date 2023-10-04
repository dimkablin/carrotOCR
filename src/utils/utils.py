""" Functions to work with environment """

import os
from src.env import project_dir


def get_abspath(path):
    """ Get the absolute path from this file and add the argument path"""
    return os.path.join(project_dir, path)
