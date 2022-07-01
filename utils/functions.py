"""
Module of helper functions
"""
import os
import shutil

import six
from pyfiglet import figlet_format
from termcolor import colored


def make_directorytree_if_not_exists(path):
    """
    Ensure a directory path exists

    Args:
        path ([type]): [description]
    """
    if not os.path.exists(path):
        os.makedirs(path)


# ToDO work out how to test command line
def log(string, color, font="slant", figlet=False):
    """Log string to cmd line

    Args:
        string ([type]): [description]
        color ([type]): [description]
        font (str, optional): [description]. Defaults to "slant".
        figlet (bool, optional): [description]. Defaults to False.
    """
    if color:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


def get_filename_from_path(filepath: str) -> str:
    """
    Strip the filename from a path eg test.sql from foobar/test.sql

    Args:
        filepath (str): [filename to get name from]

    Returns:
        str: [filename]
    """
    filename = ""

    if "/" in filepath:
        # fmt: off
        filename = filepath[filepath.rindex("/") + 1:]
        # fmt: on
    else:
        filename = filepath

    return filename


def get_filename_from_path_without_extension(filepath: str) -> str:
    """
    Strip the filename and extension from a path eg test from foobar/test.sql

    Args:
        filepath (str): [filename to get name from]

    Returns:
        str: [filename]
    """
    filename = ""

    if "/" in filepath:
        # fmt: off
        filename = filepath[filepath.rindex("/") + 1:]
        # fmt: on
    else:
        filename = filepath

    if "." in filename:
        filename = filename[: filename.rindex(".")]

    return filename


def empty_directory(folder: str) -> str:
    """[summary]

    Args:
        folder (str): [folder to empty]

    Returns:
        None
    """

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        # ToDo work out how to cause oserror to cover below with a test
        except OSError as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
