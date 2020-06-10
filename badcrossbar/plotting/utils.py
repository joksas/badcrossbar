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
        Color of the path in RGB (max value of 255 for each).
    width : float
        Width of the path.
    """
    x, y = context.get_current_point()

    context.set_line_width(width)

    rgb = tuple(i/255 for i in rgb)
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
        Color of the fill in RGB (max value of 255 for each).
    """
    x, y = context.get_current_point()

    rgb = tuple(i/255 for i in rgb)
    context.set_source_rgb(*rgb)

    context.fill()
    context.move_to(x, y)


def rgb_interpolation(array, low=0, high=1,
                      low_rgb=(180, 4, 38),
                      zero_rgb=(220, 220, 220),
                      high_rgb=(59, 76, 192)):
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
        Colour (in RGB) associated with the lower limit (max value
        of 255 for each).
    zero_rgb : tuple of int
        Colour (in RGB) associated with value of zero (max value
        of 255 for each).
    high_rgb : tuple of int
        Colour (in RGB) associated with the upper limit (max value
        of 255 for each).
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
            # TODO: differentiate between positive and negative current
            x = low_x*np.ones(array.shape)
        rgb.append(x)

    rgb = np.array(rgb)
    rgb = np.moveaxis(rgb, 0, -1)
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
