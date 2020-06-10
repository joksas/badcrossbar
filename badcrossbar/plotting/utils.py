import numpy as np
import numpy.lib.recfunctions as nlr
from sigfig import round


def complete_path(context, rgb=(0, 0, 0), width=1):
    """Completes the current path.

    Parameters
    ----------
    context : cairo.Context
        Context.
    rgb : tuple of int
        Color of the path in RGB (normalized to 1).
    width : float
        Width of the path.
    """
    x, y = context.get_current_point()

    context.set_line_width(width)

    context.set_source_rgb(*rgb)

    context.stroke()
    context.move_to(x, y)


def complete_fill(context, rgb=(0, 0, 0)):
    """Completes the current fill.

    Parameters
    ----------
    context : cairo.Context
        Context.
    rgb : tuple of int
        Color of the fill in RGB (normalized to 1).
    """
    x, y = context.get_current_point()

    context.set_source_rgb(*rgb)

    context.fill()
    context.move_to(x, y)


def rgb_interpolation(array, low=0, high=1,
                      low_rgb=(0.706, 0.016, 0.150),
                      zero_rgb=(0.865, 0.865, 0.865),
                      high_rgb=(0.230, 0.299, 0.754)):
    """Linearly interpolates RGB colors for an array in a specified range.

    Parameters
    ----------
    array : ndarray
        Arrays of values.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    low_rgb : tuple of int
        Colour (in RGB) associated with the lower limit.
    zero_rgb : tuple of int
        Colour (in RGB) associated with value of zero.
    high_rgb : tuple of int
        Colour (in RGB) associated with the upper limit.
    Returns
    -------
    ndarray of tuple of int
        RGB values associated with each of the entries in the array.
    """
    rgb = []
    for low_x, zero_x, high_x in zip(low_rgb, zero_rgb, high_rgb):
        if low != high:
            x = np.where(array > 0,
                         zero_x + (array - 0) * (high_x-zero_x)/(high-0),
                         low_x + (array - low) * (zero_x-low_x)/(0-low))
        else:
            if high > 0:
                x = high_x * np.ones(array.shape)
            else:
                x = low_x * np.ones(array.shape)
        rgb.append(x)

    rgb = np.array(rgb)
    rgb = np.moveaxis(rgb, 0, -1)
    rgb = nlr.unstructured_to_structured(rgb)
    if len(rgb.shape) == 0:
        rgb = rgb.reshape(1)
    return rgb


def rgb_single_color(shape, color=(0, 0, 0)):
    """Return array with RGB values of a single color.

    Parameters
    ----------
    shape : tuple of int
        Shape of the array.
    color : tuple of int
        RGB (normalized to 1) of the color.

    Returns
    -------
    ndarray of tuple of int
        Array with RGB values.
    """
    rgb = np.ones((*shape, len(color))) * color
    rgb = nlr.unstructured_to_structured(rgb)
    if len(rgb.shape) == 0:
        rgb = rgb.reshape(1)
    return rgb


def arrays_range(*arrays):
    """Finds the minimum and maximum value in arbitrary number of arrays.

    Parameters
    ----------
    arrays : ndarray
        Arrays.

    Returns
    -------
    tuple of float
        Minimum and maximum values in the provided arrays.
    """
    low = np.inf
    high = -np.inf

    for array in arrays:
        if array is not None:
            minimum = np.min(array)
            if minimum < low:
                low = minimum

            maximum = np.max(array)
            if maximum > high:
                high = maximum

    low = round(float(low), sigfigs=2)
    high = round(float(high), sigfigs=2)

    if np.sign(low) != np.sign(high):
        maximum_absolute = np.max([np.abs(low), np.abs(high)])
        low = -maximum_absolute
        high = maximum_absolute
    return low, high


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


def average_if_list(*arrays):
    """If an argument is a list, the function returns element-wise average of
    arrays in the list.

    Parameters
    ----------
    arrays : ndarray or list of ndarray
        Arrays or lists of arrays.

    Returns
    -------
    Potentially averaged arrays.
    """
    new_arrays = []
    for array in arrays:
        if isinstance(array, list):
            array = np.mean(array, axis=0)
        new_arrays.append(array)

    return new_arrays
