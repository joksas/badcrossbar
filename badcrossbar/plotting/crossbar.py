import numpy as np
import badcrossbar.plotting as plotting


def word_line(ctx, colors, segment_length=120, first=False):
    """Draws a word line of a crossbar array.

    Parameters
    ----------
    ctx : cairo.Context
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
            plotting.shapes.line(ctx, segment_length)
        else:
            unit = segment_length/5
            plotting.shapes.line(ctx, 2 * unit)
            plotting.shapes.semicircle(ctx, unit)
            plotting.shapes.line(ctx, 2 * unit)

        plotting.utils.complete_path(ctx, rgb=color, width=width)


def bit_line(ctx, colors, segment_length=120):
    """Draws a bit line of a crossbar array.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the bit line segments in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    """
    width = segment_length/120*3
    for color in colors:
        plotting.shapes.line(ctx, segment_length, angle=np.pi / 2)
        plotting.utils.complete_path(ctx, rgb=color, width=width)


def device_row(ctx, colors, segment_length=120):
    """Draws a row of crossbar devices.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the crossbar devices in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    """
    width = segment_length/120*5
    x, y = ctx.get_current_point()
    device_length = segment_length/2*np.sqrt(2)  # Pythagorean theorem
    for color in colors:
        x += segment_length
        ctx.move_to(x, y)
        plotting.devices.memristor(ctx, length=device_length, angle=np.pi / 4)
        plotting.utils.complete_path(ctx, rgb=color, width=width)


def nodes(ctx, colors, segment_length=120, bit_line_nodes=True):
    """Draws a row of nodes.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of int
        Colors of the nodes in RGB (max value of 255).
    segment_length : float
        The length of each segment.
    bit_line_nodes : bool
        If True, draws nodes on the bit lines.
    """
    diameter = segment_length/120*7
    x, y = ctx.get_current_point()
    if bit_line_nodes:
        x += segment_length/2
        y += segment_length/2
    radius = diameter/2
    for color in colors:
        x += segment_length
        ctx.move_to(x, y)
        ctx.arc(x, y, radius, 0, 2 * np.pi)
        ctx.move_to(x, y)
        plotting.utils.complete_fill(ctx, color)


def bit_lines(ctx, bit_line_currents, diagram_pos, low, high,
              segment_length=120, crossbar_shape=(128, 64),
              default_color=(0, 0, 0)):
    """Draws bit lines.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    bit_line_currents : ndarray
        Currents flowing through bit line segments.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float
        The length of each segment.
    crossbar_shape : tuple of int
        Shape of the crossbar array. Used when bit_line_currents is None.
    default_color : tuple of float
        The colour (in RGB) of bit lines if their currents are not provided.
    """
    x = diagram_pos[0] + 1.5*segment_length
    y = diagram_pos[1] + 0.5*segment_length
    ctx.move_to(x, y)

    if bit_line_currents is not None:
        for single_bit_line in np.transpose(bit_line_currents):
            colors = plotting.utils.rgb_interpolation(
                single_bit_line, low=low, high=high)
            bit_line(ctx, colors, segment_length=segment_length)
            x += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=default_color)
        for colors in np.transpose(colors_list):
            bit_line(ctx, colors, segment_length=segment_length)
            x += segment_length
            ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def word_lines(ctx, word_line_currents, diagram_pos, low, high,
               segment_length=120, crossbar_shape=(128, 64),
               default_color=(0, 0, 0)):
    """Draws word lines.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    word_line_currents : ndarray
        Currents flowing through word line segments.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float
        The length of each segment.
    crossbar_shape : tuple of int
        Shape of the crossbar array. Used when word_line_currents is None.
    default_color : tuple of float
        The colour (in RGB) of word lines if their currents are not provided.
    """
    x, y = diagram_pos
    ctx.move_to(x, y)

    if word_line_currents is not None:
        for idx, single_word_line in enumerate(word_line_currents):
            colors = plotting.utils.rgb_interpolation(
                single_word_line, low=low, high=high)
            if idx == 0:
                first = True
            else:
                first = False
            word_line(ctx, colors, first=first,
                      segment_length=segment_length)
            y += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=default_color)
        for idx, colors in enumerate(colors_list):
            if idx == 0:
                first = True
            else:
                first = False
            word_line(ctx, colors, first=first,
                      segment_length=segment_length)
            y += segment_length
            ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def devices(ctx, device_currents, diagram_pos, low, high,
            segment_length=120, default_color=(0, 0, 0),
            crossbar_shape=(128, 64)):
    """Draws crossbar devices and the nodes.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    device_currents : ndarray
        Currents flowing through crossbar devices.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float
        The length of each segment.
    default_color : tuple of float
        The colour (in RGB) of crossbar devices (if their currents are not
        provided), as well as of nodes.
    crossbar_shape : tuple of int
        Shape of the crossbar array. Used when device_currents is None.
    """
    x, y = diagram_pos
    ctx.move_to(x, y)

    if device_currents is not None:
        for single_device_row in device_currents:
            colors = plotting.utils.rgb_interpolation(
                single_device_row, low=low, high=high)
            device_row(ctx, colors, segment_length=segment_length)
            y += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=default_color)
        for colors in colors_list:
            device_row(ctx, colors, segment_length=segment_length)
            y += segment_length
            ctx.move_to(x, y)

    x, y = diagram_pos
    ctx.move_to(x, y)
    colors_list = plotting.utils.rgb_single_color(
        crossbar_shape, color=default_color)
    for colors in colors_list:
        for i in [True, False]:
            ctx.move_to(x, y)
            nodes(ctx, colors, bit_line_nodes=i, segment_length=segment_length)
        y += segment_length
        ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def dimensions(shape, max_dim=1000, color_bar_fraction=(0.5, 0.15),
               border_fraction=0.05):
    """Extracts dimensions of the surface.

    Parameters
    ----------
    shape : tuple of int
        Shape of the crossbar array (num_word_lines, num_bit_lines).
    max_dim : float
        The length of the longest side.
    color_bar_fraction : tuple of float
        The fraction of the surface that the color bar region will take on
        the right (vertically and horizontally.
    border_fraction : float
        Fraction of the max_dim that will be blank on all sides of the surface.

    Returns
    -------
    surface_dims : tuple of float
        Dimensions of the surface.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    segment_length : float
        The length of each segment.
    color_bar_pos : tuple of float
        Coordinates of the top left point of the color bar.
    color_bar_dims : tuple of float
        Width and height of the color bar.
    """
    adjusted_shape = (shape[0]+0.5, shape[1]+0.5)
    active_horizontal_fraction = 1 - color_bar_fraction[1] - 2 * border_fraction
    if adjusted_shape[1]/adjusted_shape[0] > active_horizontal_fraction:
        width_fraction = active_horizontal_fraction
        segment_fraction = width_fraction/adjusted_shape[1]
        height_fraction = segment_fraction*adjusted_shape[0]
        width = max_dim
        height = (height_fraction + 2 * border_fraction) * max_dim
    else:
        height_fraction = 1 - 2 * border_fraction
        segment_fraction = height_fraction/adjusted_shape[0]
        width_fraction = segment_fraction*adjusted_shape[1]
        height = max_dim
        width = (width_fraction +
                 color_bar_fraction[1] + 2 * border_fraction) * max_dim

    if height/width < (color_bar_fraction[0] + 2 * border_fraction):
        height = max_dim * (color_bar_fraction[0] + 2 * border_fraction)

    segment_length = segment_fraction * max_dim

    x_start = border_fraction * max_dim
    y_start = height/2 - adjusted_shape[0]*segment_length/2
    diagram_pos = (x_start, y_start)
    surface_dims = (width, height)
    color_bar_pos, color_bar_dims = plotting.color_bar.dimensions(
        surface_dims, color_bar_fraction, border_fraction)
    return surface_dims, diagram_pos, segment_length,\
        color_bar_pos, color_bar_dims
