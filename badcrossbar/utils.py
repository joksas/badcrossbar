import os
import pickle
from datetime import datetime

import numpy as np
from pathvalidate import sanitize_filepath


def unique_path(path, extension="pdf", sanitize=True):
    """Append a number to the path, if it is not unique.

    Parameters
    ----------
    path : str
        Path of the filename without the extension.
    extension : str, optional
        File extension.
    sanitize : bool, optional
        If True, sanitizes the filename by removing illegal characters and
        making the path compatible with the operating system.

    Returns
    -------
    str
        Unique path.
    """
    if sanitize:
        path = sanitize_filepath(path, platform="auto")

    full_path = "{}.{}".format(path, extension)
    if os.path.exists(full_path):
        number = 1
        while True:
            number += 1
            new_full_path = "{}-{}.{}".format(path, number, extension)
            if os.path.exists(new_full_path):
                continue
            else:
                full_path = new_full_path
                break

    return full_path


def time(keep_ms=False):
    """Returns current time.

    Parameters
    ----------
    keep_ms : bool, optional
        If True, includes milliseconds.
    Returns
    -------
    str
        Current time.
    """
    time_str = str(datetime.now())
    if keep_ms is False:
        time_str = time_str.split(".")[0]
    return time_str


def squeeze_third_axis(array):
    """Removes third axis of ndarray if it has shape of 1.

    Parameters
    ----------
    array : ndarray
        3D array.

    Returns
    -------
    ndarray
        2D or 3D array.
    """
    if array.ndim == 3:
        if array.shape[2] == 1:
            array = np.squeeze(array, axis=2)

    return array


def average_if_3D(array):
    """If array is 3D, it is averaged along the third axis.

    Parameters
    ----------
    array : ndarray
        2D or 3D array.

    Returns
    -------
    ndarray
        2D array.
    """
    if array.ndim == 3:
        array = np.mean(array, axis=2)

    return array


def message(message_str, **kwargs):
    """Prints current time followed by a gap and a custom message.

    Parameters
    ----------
    message_str : str
        Message to be printed at the end of the line.
    **kwargs
        verbose : int, optional
            The message is shown only is verbose is equal to 1.
        show_time : bool, optional
            If True, prints out current time.
    """
    if kwargs.get("verbose", 1) == 1:
        if kwargs.get("show_time", True):
            message_str = (
                time(kwargs.get("keep_ms", False)) + gap(kwargs.get("gap_size", 5)) + message_str
            )
        print(message_str)


def gap(gap_size=5):
    """Returns a given number of whitespace characters.

    Parameters
    ----------
    gap_size : int, optional
        Number of whitespace characters to be printed.

    Returns
    -------
    str
        Whitespace.
    """
    gap_str = gap_size * " "
    return gap_str


def arrays_shape(*arrays):
    """Returns the shape of the first array that is not None.

    Parameters
    ----------
    arrays : ndarray
        Arrays.

    Returns
    -------
    tuple of int
        Shape.
    """
    for array in arrays:
        if array is not None:
            shape = array.shape
            return shape


def save_pickle(variable, path, allow_overwrite=False, verbose=False, sanitize=True):
    """Saves variable to a pickle file.

    Parameters
    ----------
    variable : any
        Variable to be saved.
    path : str
        Path to the pickle file, excluding extension.
    allow_overwrite : bool, optional
        If False, will not check for existing files with the same name and
        will overwrite if such files exist.
    verbose : bool, optional
        If True, notifies the user that the file has been saved.
    sanitize : bool, optional
        If True, sanitizes the filename by removing illegal characters and
        making the path compatible with the operating system.
    """
    if sanitize:
        path = sanitize_filepath(path, platform="auto")

    if allow_overwrite:
        path = "{}.pickle".format(path)
    else:
        path = unique_path(path, "pickle")

    with open(path, "wb") as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if verbose:
        print("Saved {}.".format(path))


def load_pickle(path, sanitize=True):
    """Loads pickle file.

    Parameters
    ----------
    path : str
        Path to the pickle file, including extension.
    sanitize : bool, optional
        If True, sanitizes the filename by removing illegal characters and
        making the path compatible with the operating system.

    Returns
    -------
    any
        Extracted contents.
    """
    if sanitize:
        path = sanitize_filepath(path, platform="auto")

    with open(path, "rb") as handle:
        variable = pickle.load(handle)

    return variable


def distributed_array(flattened_array, model_array):
    """Reshapes flattened array.

    Parameters
    ----------
    flattened_array : ndarray
        An array whose each column contains a flattened array.
    model_array : ndarray
        An array whose shape is used for reshaping.

    Returns
    -------
    ndarray
        Array or a list of arrays in specified shape.
    """
    reshaped_i = flattened_array.reshape(
        (model_array.shape[0], model_array.shape[1], flattened_array.shape[1])
    )
    reshaped_i = squeeze_third_axis(reshaped_i)

    return reshaped_i
