import cairo
import numpy as np
import badcrossbar.plotting.utils as utils
import badcrossbar.plotting.crossbar as crossbar
import badcrossbar.plotting.dimensions as mydimensions


def currents(device_currents, word_line_currents, bit_line_currents):
    dimensions, pos_start, segment_length, color_bar_dims = mydimensions.get(
        device_currents.shape, max_dimension=1000)
    surface = cairo.PDFSurface('crossbar_currents.pdf', *dimensions)
    ctx = cairo.Context(surface)

    low, high = utils.arrays_range(
        device_currents, word_line_currents, bit_line_currents)

    bit_lines(ctx, bit_line_currents, *pos_start, low, high,
              segment_length=segment_length)

    word_lines(ctx, word_line_currents, *pos_start, low, high,
               segment_length=segment_length)

    devices(ctx, device_currents, *pos_start, low, high,
            segment_length=segment_length, node_color=(0, 0, 0))

    color_bar(ctx, color_bar_dims, low, high)


def bit_lines(context, bit_line_currents, x_start, y_start, low, high,
              segment_length=120):
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
    width : float
        Width of the path.
    """
    x, y = x_start + 1.5*segment_length, y_start + 0.5*segment_length
    context.move_to(x, y)

    for bit_line in np.transpose(bit_line_currents):
        colors = utils.rgb_interpolation(bit_line, low=low, high=high)
        crossbar.bit_line(context, colors,
                          segment_length=segment_length)
        x += segment_length
        context.move_to(x, y)

    context.move_to(x_start, y_start)


def word_lines(context, word_line_currents, x_start, y_start, low, high,
               segment_length=120):
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
    width : float
        Width of the path.
    """
    x, y = x_start, y_start
    context.move_to(x, y)

    for idx, word_line in enumerate(word_line_currents):
        colors = utils.rgb_interpolation(word_line, low=low, high=high)
        if idx == 0:
            first = True
        else:
            first = False
        crossbar.word_line(context, colors, first=first,
                           segment_length=segment_length)
        y += segment_length
        context.move_to(x, y)

    context.move_to(x_start, y_start)


def devices(context, device_currents, x_start, y_start, low, high,
            segment_length=120, node_color=(0, 0, 0)):
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
    width : float
        Width of the path.
    node_color : tuple of int
        Color of the node in RGB.
    node_diameter : float
        Diameter of the node.
    """
    x, y = x_start, y_start
    context.move_to(x, y)
    for device_row in device_currents:
        colors = utils.rgb_interpolation(device_row, low=low, high=high)
        crossbar.device_row(context, colors, segment_length=segment_length)

        colors = utils.rgb_interpolation(np.zeros(device_row.shape),
                                         low_rgb=node_color,
                                         zero_rgb=node_color,
                                         high_rgb=node_color, low=1)
        for i in [True, False]:
            context.move_to(x, y)
            crossbar.nodes(context, colors, bit_line_nodes=i,
                           segment_length=segment_length)
        y += segment_length
        context.move_to(x, y)

    context.move_to(x_start, y_start)


def color_bar(context, color_bar_dims, low, high):
    context.rectangle(*color_bar_dims)
    pattern = cairo.LinearGradient(color_bar_dims[0], color_bar_dims[1],
                                   color_bar_dims[0] + color_bar_dims[2],
                                   color_bar_dims[1] + color_bar_dims[3])

    top_rgb = utils.rgb_interpolation(np.array([high]), low=low, high=high)[0]
    if low != high:
        middle_rgb = utils.rgb_interpolation(
            np.array([0]), low=low, high=high)[0]
    else:
        middle_rgb = utils.rgb_interpolation(
            np.array([0]), low=-1, high=1)[0]
    bottom_rgb = utils.rgb_interpolation(np.array([low]), low=low, high=high)[0]

    context.set_source_rgb(0, 0, 0)
    font_size = color_bar_dims[2]/3
    context.set_font_size(font_size)

    if low < 0 < high:
        pattern.add_color_stop_rgb(0, *top_rgb)
        pattern.add_color_stop_rgb(0.5, *middle_rgb)
        pattern.add_color_stop_rgb(1, *bottom_rgb)

        x = color_bar_dims[0] + color_bar_dims[2]*1.2
        y = color_bar_dims[1] + 0.5*font_size
        context.move_to(x, y)
        context.show_text(str(high))

        x = color_bar_dims[0] + color_bar_dims[2]*1.2
        y = color_bar_dims[1] + 0.5*color_bar_dims[3] + 0.5*font_size
        context.move_to(x, y)
        context.show_text(str(0))

        x = color_bar_dims[0] + color_bar_dims[2]*1.2
        y = color_bar_dims[1] + color_bar_dims[3] + 0.5*font_size
        context.move_to(x, y)
        context.show_text(str(low))
    else:
        if high > 0:
            pattern.add_color_stop_rgb(0, *top_rgb)
            pattern.add_color_stop_rgb(1, *middle_rgb)

            x = color_bar_dims[0] + color_bar_dims[2]*1.2
            y = color_bar_dims[1] + 0.5*font_size
            context.move_to(x, y)
            context.show_text(str(high))

            x = color_bar_dims[0] + color_bar_dims[2]*1.2
            y = color_bar_dims[1] + color_bar_dims[3] + 0.5*font_size
            context.move_to(x, y)
            context.show_text(str(0))
        else:
            pattern.add_color_stop_rgb(0, *middle_rgb)
            pattern.add_color_stop_rgb(1, *bottom_rgb)

            x = color_bar_dims[0] + color_bar_dims[2]*1.2
            y = color_bar_dims[1] + 0.5*font_size
            context.move_to(x, y)
            context.show_text(str(0))

            x = color_bar_dims[0] + color_bar_dims[2]*1.2
            y = color_bar_dims[1] + color_bar_dims[3] + 0.5*font_size
            context.move_to(x, y)
            context.show_text(str(low))

    context.set_source(pattern)
    context.fill()


