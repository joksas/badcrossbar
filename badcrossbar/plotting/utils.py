import numpy as np
import numpy.lib.recfunctions as nlr


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


def rgb_interpolation(array, low=0, high=1,
                      low_rgb=(0, 0, 0), high_rgb=(255, 255, 255)):
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
    high_rgb : tuple of int
        Colour (in RGB) associated with the upper limit (max value
        of 255 for each).
    Returns
    -------
    ndarray of tuple of int
        RGB values associated with each of the entries in the array.
    """
    rgb = []
    for low_x, high_x in zip(low_rgb, high_rgb):
        x = low_x + (array - low) * (high_x-low_x)/(high-low)
        rgb.append(x)

    rgb = np.array(rgb)
    rgb = np.moveaxis(rgb, 0, -1)
    rgb = nlr.unstructured_to_structured(rgb)
    return rgb
