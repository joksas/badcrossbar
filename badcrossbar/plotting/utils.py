import cairo
import numpy as np
import numpy.lib.recfunctions as nlr
import numpy.typing as npt
from badcrossbar import utils
from pathvalidate import sanitize_filepath
from sigfig import round


def complete_path(
    ctx: cairo.Context, rgb: tuple[float, float, float] = (0, 0, 0), width: float = 1
):
    """Completes the current path.

    Args:
        ctx: Context.
        width: Width of the path.
        rgb: Normalized RGB value of the path.
    """
    x, y = ctx.get_current_point()

    ctx.set_line_width(width)
    ctx.set_source_rgb(*rgb)

    ctx.stroke()

    ctx.move_to(x, y)


def complete_fill(ctx: cairo.Context, rgb: tuple[float, float, float] = (0, 0, 0)):
    """Completes the current fill.

    Args:
        ctx: Context.
        rgb: Normalized RGB value of the path.
    """
    x, y = ctx.get_current_point()

    ctx.set_source_rgb(*rgb)

    ctx.fill()

    ctx.move_to(x, y)


def rgb_interpolation(
    array: npt.NDArray,
    low: float = 0,
    high: float = 1,
    low_rgb: tuple[float, float, float] = (213 / 255, 94 / 255, 0 / 255),
    zero_rgb: tuple[float, float, float] = (235 / 255, 235 / 255, 235 / 255),
    high_rgb: tuple[float, float, float] = (0 / 255, 114 / 255, 178 / 255),
) -> npt.NDArray[tuple[float, float, float]]:
    """Linearly interpolates RGB colors for an array in a specified range.

    Args:
        array: Array of values.
        low: Lower limit of the linear range.
        high: Upper limit of the linear range.
        low_rgb: Colour (in RGB) associated with the lower limit.
        zero_rgb: Colour (in RGB) associated with value of zero.
        high_rgb: Colour (in RGB) associated with the upper limit.

    Returns:
        RGB values associated with each of the entries in the array.
    """
    rgb = []
    if low == 0:
        low = -1
    if high == 0:
        high = 1

    for low_x, zero_x, high_x in zip(low_rgb, zero_rgb, high_rgb):
        # linearly interpolate in two intervals (above and below zero)
        x = np.where(
            array > 0,
            zero_x + (array - 0) * (high_x - zero_x) / (high - 0),
            low_x + (array - low) * (zero_x - low_x) / (0 - low),
        )

        rgb.append(x)

    # return ndarray of RGB tuples
    rgb = np.array(rgb)
    rgb = np.moveaxis(rgb, 0, -1)
    rgb = nlr.unstructured_to_structured(rgb)
    if len(rgb.shape) == 0:
        rgb = rgb.reshape(1)
    return rgb


def rgb_single_color(shape: tuple[int, int], color: tuple[float, float, float] = (0, 0, 0)):
    """Return array with RGB values of a single color.

    Args:
        shape: Shape of the array.
        color: RGB (normalized to 1) of the color.

    Returns:
        Array with RGB values.
    """
    rgb = np.ones((*shape, len(color))) * color
    rgb = nlr.unstructured_to_structured(rgb)
    if len(rgb.shape) == 0:
        rgb = rgb.reshape(1)
    return rgb


def arrays_range(*arrays: list[np.ndarray], sf: int = 2) -> tuple[float, float]:
    """Finds the color bar range from arbitrary number of arrays.

    Args:
        arrays: Arrays.
        sf: Number of significant figures.

    Returns:
        Minimum and maximum values in the color bar.
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

    # if 0, make sure that `low` and `high` are int
    if low == 0:
        low = 0
    if high == 0:
        high = 0

    # round to specified number of significant figures
    if low != 0:
        low = round(float(low), sigfigs=sf)
    if high != 0:
        high = round(float(high), sigfigs=sf)

    # if the range captures both positive and negative numbers, make it
    # symmetrical around 0
    if np.sign(low) != np.sign(high) and low != 0 and high != 0:
        maximum_absolute = np.max([np.abs(low), np.abs(high)])
        low = -maximum_absolute
        high = maximum_absolute
    return low, high


def set_defaults(kwargs, branches: bool = True):
    """Sets default values for kwargs arguments in `badcrossbar.plot` functions.

    Args:
        kwargs: Optional keyword arguments.
        branches: Whether branches are being plotted. If `False`, it is assumed
            that nodes are being plotted.

    Returns:
        Optional keyword arguments with the default values set.
    """
    kwargs.setdefault("default_color", (0, 0, 0))
    kwargs.setdefault("wire_scaling_factor", 1)
    kwargs.setdefault("device_scaling_factor", 1)
    kwargs.setdefault("axis_label", "Current (A)")
    kwargs.setdefault("low_rgb", (213 / 255, 94 / 255, 0 / 255))
    kwargs.setdefault("zero_rgb", (235 / 255, 235 / 255, 235 / 255))
    kwargs.setdefault("high_rgb", (0 / 255, 114 / 255, 178 / 255))
    kwargs.setdefault("allow_overwrite", False)
    kwargs.setdefault("device_type", "memristor")
    kwargs.setdefault("significant_figures", 2)
    kwargs.setdefault("round_crossings", True)
    kwargs.setdefault("width", 210)
    if branches:
        kwargs.setdefault("node_scaling_factor", 1)
        kwargs.setdefault("filename", "crossbar-currents")
    else:
        kwargs.setdefault("node_scaling_factor", 1.4)
        kwargs.setdefault("filename", "crossbar-voltages")

    return kwargs


def get_filepath(filename: str, allow_overwrite: bool):
    """Constructs filepath of the diagram.

    Args:
        filename: Filename (without the extension).
        allow_overwrite: If True, can overwrite existing PDF files with the same name.

    Returns:
        Filepath of the diagram.
    """
    extension = "pdf"

    if allow_overwrite:
        filepath = f"{filename}.{extension}"
        filepath = sanitize_filepath(filepath)
    else:
        filepath = utils.unique_path(filename, extension)

    return filepath
