import os
import pickle
from datetime import datetime

import numpy as np
import numpy.typing as npt
from pathvalidate import sanitize_filepath


def unique_path(path: str, extension: str = "pdf", sanitize: bool = True) -> str:
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

    full_path = f"{path}.{extension}"
    if os.path.exists(full_path):
        number = 1
        while True:
            number += 1
            new_full_path = f"{path}-{number}.{extension}"
            if os.path.exists(new_full_path):
                continue
            else:
                full_path = new_full_path
                break

    return full_path


def squeeze_third_axis(array: npt.NDArray) -> npt.NDArray:
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


def average_if_3D(array: npt.NDArray) -> npt.NDArray:
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


def arrays_shape(*arrays: list[npt.NDArray]):
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


def save_pickle(
    variable, path: str, allow_overwrite: bool = False, verbose: bool = False, sanitize: bool = True
):
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
        path = f"{path}.pickle"
    else:
        path = unique_path(path, "pickle")

    with open(path, "wb") as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if verbose:
        print(f"Saved {path}.")


def load_pickle(path: str, sanitize: bool = True):
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


def distributed_array(flattened_array: npt.NDArray, model_array: npt.NDArray) -> npt.NDArray:
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
