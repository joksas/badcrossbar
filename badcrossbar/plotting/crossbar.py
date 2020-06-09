import numpy as np
import badcrossbar.plotting.shapes as shapes
import badcrossbar.plotting.devices as devices
import badcrossbar.plotting.utils as utils


def word_line(context, colors, width=1, segment_length=120, first=False):
    """Draws a word line of a crossbar array.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the word line segments in RGB (max value of 255).
    width : float
        Width of the path.
    segment_length : float
        The length of each segment.
    first : bool
        If True, draws the first (from the top) word line.
    """
    for idx, color in enumerate(colors):
        if idx == 0 or first:
            shapes.line(context, segment_length)
        else:
            unit = segment_length/4
            shapes.line(context, 1.5*unit)
            shapes.semicircle(context, unit)
            shapes.line(context, 1.5*unit)

        utils.complete_path(context, rgb=color, width=width)


def bit_line(context, colors, width=1, segment_length=120):
    """Draws a bit line of a crossbar array.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the bit line segments in RGB (max value of 255).
    width : float
        Width of the path.
    segment_length : float
        The length of each segment.
    """
    for color in colors:
        shapes.line(context, segment_length, angle=np.pi/2)
        utils.complete_path(context, rgb=color, width=width)


def device_row(context, colors, width=5, segment_length=120):
    """Draws a row of crossbar devices.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the crossbar devices in RGB (max value of 255).
    width : float
        Width of the path.
    segment_length : float
        The length of each segment.
    """
    x, y = context.get_current_point()
    device_length = segment_length/2*np.sqrt(2)  # Pythagorean theorem
    for color in colors:
        x += segment_length
        context.move_to(x, y)
        devices.memristor(context, length=device_length, angle=np.pi/4)
        utils.complete_path(context, rgb=color, width=width)


def nodes(context, colors, diameter=7, segment_length=120, bit_line_nodes=True):
    """Draws a row of nodes.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the nodes in RGB (max value of 255).
    diameter : float
        Diameter of the nodes.
    segment_length : float
        The length of each segment.
    bit_line_nodes : bool
        If True, draws nodes on the bit lines.
    """
    x, y = context.get_current_point()
    if bit_line_nodes:
        x += segment_length/2
        y += segment_length/2
    radius = diameter/2
    for color in colors:
        x += segment_length
        context.move_to(x, y)
        context.arc(x, y, radius, 0, 2*np.pi)
        context.move_to(x, y)
        utils.complete_fill(context, color)
