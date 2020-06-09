import numpy as np
import badcrossbar.plotting.shapes as shapes
import badcrossbar.plotting.utils as utils


def bit_line(context, colors, width=1, segment_length=150):
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
        The length of regular (not the bottom one) bit line segments).
    """
    num_segments = len(colors)

    for idx, color in enumerate(colors):
        if idx+1 == num_segments:
            segment_length *= 4/3

        shapes.line(context, segment_length, angle=np.pi/2)
        utils.complete_path(context, rgb=color, width=width)