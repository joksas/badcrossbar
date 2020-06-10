import numpy as np
import badcrossbar.plotting as plotting


def word_line(context, colors, segment_length=120, first=False):
    """Draws a word line of a crossbar array.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the word line segments in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    first : bool
        If True, draws the first (from the top) word line.
    """
    width = segment_length/120*3
    for idx, color in enumerate(colors):
        if idx == 0 or first:
            plotting.shapes.line(context, segment_length)
        else:
            unit = segment_length/5
            plotting.shapes.line(context, 2*unit)
            plotting.shapes.semicircle(context, unit)
            plotting.shapes.line(context, 2*unit)

        plotting.utils.complete_path(context, rgb=color, width=width)


def bit_line(context, colors, segment_length=120):
    """Draws a bit line of a crossbar array.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the bit line segments in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    """
    width = segment_length/120*3
    for color in colors:
        plotting.shapes.line(context, segment_length, angle=np.pi/2)
        plotting.utils.complete_path(context, rgb=color, width=width)


def device_row(context, colors, segment_length=120):
    """Draws a row of crossbar devices.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the crossbar devices in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    """
    width = segment_length/120*5
    x, y = context.get_current_point()
    device_length = segment_length/2*np.sqrt(2)  # Pythagorean theorem
    for color in colors:
        x += segment_length
        context.move_to(x, y)
        plotting.devices.memristor(context, length=device_length, angle=np.pi/4)
        plotting.utils.complete_path(context, rgb=color, width=width)


def nodes(context, colors, segment_length=120, bit_line_nodes=True):
    """Draws a row of nodes.

    Parameters
    ----------
    context : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the nodes in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    bit_line_nodes : bool
        If True, draws nodes on the bit lines.
    """
    diameter = segment_length/120*7
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
        plotting.utils.complete_fill(context, color)


def bit_lines(context, bit_line_currents, x_start, y_start, low, high,
              segment_length=120, crossbar_shape=(128, 64)):
    """Draws bit lines.

    Parameters
    ----------
    context : cairo.Context
        Context.
    bit_line_currents : ndarray
        Currents flowing through bit line segments.
    x_start : float
        x coordinate of the top left point of the diagram.
    y_start : float
        x coordinate of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float
        The length of each segment.
    crossbar_shape : tuple of int
        Shape of the crossbar array. Used when bit_line_currents is None.
    """
    x, y = x_start + 1.5*segment_length, y_start + 0.5*segment_length
    context.move_to(x, y)

    if bit_line_currents is not None:
        for single_bit_line in np.transpose(bit_line_currents):
            colors = plotting.utils.rgb_interpolation(
                single_bit_line, low=low, high=high)
            bit_line(context, colors, segment_length=segment_length)
            x += segment_length
            context.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=(0, 0, 0))
        for colors in np.transpose(colors_list):
            bit_line(context, colors, segment_length=segment_length)
            x += segment_length
            context.move_to(x, y)

    context.move_to(x_start, y_start)


def word_lines(context, word_line_currents, x_start, y_start, low, high,
               segment_length=120, crossbar_shape=(128, 64)):
    """Draws word lines.

    Parameters
    ----------
    context : cairo.Context
        Context.
    word_line_currents : ndarray
        Currents flowing through word line segments.
    x_start : float
        x coordinate of the top left point of the diagram.
    y_start : float
        x coordinate of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float
        The length of each segment.
    crossbar_shape : tuple of int
        Shape of the crossbar array. Used when word_line_currents is None.
    """
    x, y = x_start, y_start
    context.move_to(x, y)

    if word_line_currents is not None:
        for idx, single_word_line in enumerate(word_line_currents):
            colors = plotting.utils.rgb_interpolation(
                single_word_line, low=low, high=high)
            if idx == 0:
                first = True
            else:
                first = False
            word_line(context, colors, first=first,
                      segment_length=segment_length)
            y += segment_length
            context.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(crossbar_shape, color=(0, 0, 0))
        for idx, colors in enumerate(colors_list):
            if idx == 0:
                first = True
            else:
                first = False
            word_line(context, colors, first=first,
                      segment_length=segment_length)
            y += segment_length
            context.move_to(x, y)

    context.move_to(x_start, y_start)


def devices(context, device_currents, x_start, y_start, low, high,
             segment_length=120, node_color=(0, 0, 0), crossbar_shape=(128, 64)):
    """Draws crossbar devices and the nodes.

    Parameters
    ----------
    context : cairo.Context
        Context.
    device_currents : ndarray
        Currents flowing through crossbar devices.
    x_start : float
        x coordinate of the top left point of the diagram.
    y_start : float
        x coordinate of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float
        The length of each segment.
    node_color : tuple of int
        Color of the node in RGB.
    crossbar_shape : tuple of int
        Shape of the crossbar array. Used when device_currents is None.
    """
    x, y = x_start, y_start
    context.move_to(x, y)

    if device_currents is not None:
        for single_device_row in device_currents:
            colors = plotting.utils.rgb_interpolation(
                single_device_row, low=low, high=high)
            device_row(context, colors, segment_length=segment_length)
            y += segment_length
            context.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=node_color)
        for colors in colors_list:
            plotting.crossbar.device_row(
                context, colors, segment_length=segment_length)
            y += segment_length
            context.move_to(x, y)

    x, y = x_start, y_start
    context.move_to(x, y)
    colors_list = plotting.utils.rgb_single_color(
        crossbar_shape, color=node_color)
    for colors in colors_list:
        for i in [True, False]:
            context.move_to(x, y)
            plotting.crossbar.nodes(context, colors, bit_line_nodes=i,
                                    segment_length=segment_length)
        y += segment_length
        context.move_to(x, y)

    context.move_to(x_start, y_start)


def get(shape, max_dimension=1000, color_bar_fraction=(0.5, 0.15),
        border=0.05):
    adjusted_shape = (shape[0]+0.5, shape[1]+0.5)
    active_horizontal_fraction = 1 - color_bar_fraction[1] - 2 * border
    if adjusted_shape[1]/adjusted_shape[0] > active_horizontal_fraction:
        width_fraction = active_horizontal_fraction
        segment_fraction = width_fraction/adjusted_shape[1]
        height_fraction = segment_fraction*adjusted_shape[0]
        width = max_dimension
        height = (height_fraction + 2*border)*max_dimension
    else:
        height_fraction = 1 - 2*border
        segment_fraction = height_fraction/adjusted_shape[0]
        width_fraction = segment_fraction*adjusted_shape[1]
        height = max_dimension
        width = (width_fraction +
                 color_bar_fraction[1] + 2*border) * max_dimension

    if height/width < (color_bar_fraction[0] + 2*border):
        height = max_dimension * (color_bar_fraction[0] + 2*border)

    segment_length = segment_fraction*max_dimension

    x_start = border*max_dimension
    y_start = height/2 - adjusted_shape[0]*segment_length/2
    pos_start = (x_start, y_start)
    dimensions = (width, height)
    color_bar_dims = plotting.color_bar.dimensions(
        dimensions, color_bar_fraction, border)
    return dimensions, pos_start, segment_length, color_bar_dims