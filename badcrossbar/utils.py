import os
from datetime import datetime


def unique_path(path, extension='pdf'):
    """Append a number to the path, if it is not unique.

    Parameters
    ----------
    path : str
        Path of the filename without the extension.
    extension : str
        File extension.

    Returns
    -------
    str
        Unique path.
    """
    full_path = '{}.{}'.format(path, extension)
    if os.path.exists(full_path):
        number = 1
        while True:
            number += 1
            new_full_path = '{}-{}.{}'.format(path, number, extension)
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
    keep_ms : bool
        If True, includes milliseconds.
    Returns
    -------
    str
        Current time.
    """
    time_str = str(datetime.now())
    if keep_ms is False:
        time_str = time_str.split('.')[0]
    return time_str
