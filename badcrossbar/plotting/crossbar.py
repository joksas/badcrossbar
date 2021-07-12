import numpy as np
import badcrossbar.plotting as plotting


def draw_word_line(ctx, colors, segment_length=100, round_middle=False,
                   scaling_factor=1):
    """Draws a word line of a crossbar array.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of float
        Normalized RGB values of the word line segments.
    segment_length : float, optional
        The length of each segment.
    round_middle : bool, optional
        If True, draws a semicircle midway between each two neighbouring
        nodes, instead of a straight line.
    scaling_factor : float, optional
        Scaling factor for the width.
    """
    width = segment_length/100*3*scaling_factor
    for idx, color in enumerate(colors):
        if idx == 0 or not round_middle:
            plotting.shapes.line(ctx, segment_length)
        else:
            unit = segment_length/5
            plotting.shapes.line(ctx, 2 * unit)
            plotting.shapes.semicircle(ctx, unit)
            plotting.shapes.line(ctx, 2 * unit)

        plotting.utils.complete_path(ctx, rgb=color, width=width)


def draw_bit_line(ctx, colors, segment_length=100, scaling_factor=1):
    """Draws a bit line of a crossbar array.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of float
        Normalized RGB values of the bit line segments.
    segment_length : float, optional
        The length of each segment.
    scaling_factor : float, optional
        Scaling factor for the width.
    """
    width = segment_length/100*3*scaling_factor
    for color in colors:
        plotting.shapes.line(ctx, segment_length, angle=np.pi / 2)
        plotting.utils.complete_path(ctx, rgb=color, width=width)


def draw_device_row(ctx, colors, segment_length=100, scaling_factor=1,
                    device='memristor'):
    """Draws a row of crossbar devices.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of float
        Normalized RGB values of the crossbar devices.
    segment_length : float, optional
        The length of each segment.
    scaling_factor : float, optional
        Scaling factor for the width.
    device : {'memristor', 'memristor_2', 'resistor_usa', 'resistor_europe'}, optional
        Device type to be drawn.
    """
    width = segment_length/100*5*scaling_factor
    x, y = ctx.get_current_point()
    device_length = segment_length/2*np.sqrt(2)  # Pythagorean theorem

    device_functions = {'memristor': plotting.devices.memristor,
            'memristor_2': plotting.devices.memristor_2,
            'resistor_usa': plotting.devices.resistor_usa,
            'resistor_europe': plotting.devices.resistor_europe}
    if device in device_functions:
        device_function = device_functions[device]
    else:
        raise ValueError('Device \'{}\' is not currently supported!'.format(
            device))

    for color in colors:
        x += segment_length
        ctx.move_to(x, y)
        device_function(ctx, length=device_length, angle=np.pi/4, width=width, rgb=color)


def draw_node_row(ctx, colors, segment_length=100, bit_line_nodes=True,
                  scaling_factor=1, device='memristor'):
    """Draws a row of nodes.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    colors : list of tuple of float
        Normalized RGB values of the nodes.
    segment_length : float, optional
        The length of each segment.
    bit_line_nodes : bool, optional
        If True, draws nodes on the bit lines.
    scaling_factor : float, optional
        Scaling factor for the diameter.
    device : {'memristor', 'memristor_2', 'resistor_usa', 'resistor_europe'}, optional
        Device type to be drawn (affects node diameter).
    """
    diameter = segment_length/100*7*scaling_factor
    if device in ['resistor_usa', 'resistor_europe', 'memristor_2']:
        diameter *= 5/7
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


def bit_lines(ctx, bit_line_vals, diagram_pos, low, high,
              segment_length=120, crossbar_shape=(128, 64), **kwargs):
    """Draws bit lines.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    bit_line_vals : ndarray or None
        Values associated with the interconnect segments along the bit lines.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float, optional
        The length of each segment.
    crossbar_shape : tuple of int, optional
        Shape of the crossbar array. Used when `bit_line_vals` is None.
    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the bit lines if their values are not
            provided.
    """
    x = diagram_pos[0] + 1.5*segment_length
    y = diagram_pos[1] + 0.5*segment_length
    ctx.move_to(x, y)

    if bit_line_vals is not None:
        for single_bit_line_vals in np.transpose(bit_line_vals):
            colors = plotting.utils.rgb_interpolation(
                single_bit_line_vals, low=low, high=high,
                low_rgb=kwargs.get('low_rgb'), zero_rgb=kwargs.get('zero_rgb'),
                high_rgb=kwargs.get('high_rgb'))
            draw_bit_line(ctx, colors, segment_length=segment_length,
                          scaling_factor=kwargs.get('wire_scaling_factor'))
            x += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=kwargs.get('default_color'))
        for colors in np.transpose(colors_list):
            draw_bit_line(ctx, colors, segment_length=segment_length,
                          scaling_factor=kwargs.get('wire_scaling_factor'))
            x += segment_length
            ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def word_lines(ctx, word_line_vals, diagram_pos, low, high,
               segment_length=120, crossbar_shape=(128, 64), **kwargs):
    """Draws word lines.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    word_line_vals : ndarray or None
        Values associated with the interconnect segments along the word lines.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float, optional
        The length of each segment.
    crossbar_shape : tuple of int, optional
        Shape of the crossbar array. Used when `word_line_vals` is None.
    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the word lines if their values are not
            provided.
    """
    x, y = diagram_pos
    ctx.move_to(x, y)

    if word_line_vals is not None:
        for idx, single_word_line_vals in enumerate(word_line_vals):
            colors = plotting.utils.rgb_interpolation(
                single_word_line_vals, low=low, high=high,
                low_rgb=kwargs.get('low_rgb'), zero_rgb=kwargs.get('zero_rgb'),
                high_rgb=kwargs.get('high_rgb'))
            if idx == 0:
                round_middle = False
            else:
                round_middle = kwargs.get('round_crossings')
            draw_word_line(ctx, colors, round_middle=round_middle,
                           segment_length=segment_length,
                           scaling_factor=kwargs.get('wire_scaling_factor'))
            y += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=kwargs.get('default_color'))
        for idx, colors in enumerate(colors_list):
            if idx == 0:
                round_middle = False
            else:
                round_middle = kwargs.get('round_crossings')
            draw_word_line(ctx, colors, round_middle=round_middle,
                           segment_length=segment_length,
                           scaling_factor=kwargs.get('wire_scaling_factor'))
            y += segment_length
            ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def devices(ctx, device_vals, diagram_pos, low, high, segment_length=120,
            crossbar_shape=(128, 64), **kwargs):
    """Draws crossbar devices.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    device_vals : ndarray or None
        Values associated with crossbar devices.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float, optional
        The length of each segment.
    crossbar_shape : tuple of int, optional
        Shape of the crossbar array. Used when `device_vals` is None.
    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the crossbar devices if their values
            are not provided.
    """
    x, y = diagram_pos
    ctx.move_to(x, y)

    if device_vals is not None:
        for device_row_vals in device_vals:
            colors = plotting.utils.rgb_interpolation(
                device_row_vals, low=low, high=high,
                low_rgb=kwargs.get('low_rgb'), zero_rgb=kwargs.get('zero_rgb'),
                high_rgb=kwargs.get('high_rgb'))
            draw_device_row(ctx, colors, segment_length=segment_length,
                            scaling_factor=kwargs.get('device_scaling_factor'),
                            device=kwargs.get('device_type'))
            y += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=kwargs.get('default_color'))
        for colors in colors_list:
            draw_device_row(ctx, colors, segment_length=segment_length,
                            scaling_factor=kwargs.get('device_scaling_factor'),
                            device=kwargs.get('device_type'))
            y += segment_length
            ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def nodes(ctx, node_vals, diagram_pos, low, high, segment_length=120,
          crossbar_shape=(128, 64), bit_line=False, **kwargs):
    """Draws nodes.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    node_vals : ndarray or None
        Values associated with the nodes.
    diagram_pos : tuple of float
        Coordinates of the top left point of the diagram.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    segment_length : float, optional
        The length of each segment.
    crossbar_shape : tuple of int, optional
        Shape of the crossbar array. Used when `node_vals` is None.
    bit_line : bool, optional
        If True, draws nodes on the bit lines.
    kwargs
        device_scaling_factor : float, optional
            Scaling factor for the width of the devices. Also scales the nodes.
        node_scaling_factor : float, optional
            Scaling factor for the diameter of the nodes which is combined
            with `device_scaling_factor`. For example, if one wanted to only
            scale the device width by a factor of 2, but keep the node diameter
            the same, arguments `device_scaling_factor = 2` and
            `node_scaling_factor = 1/2` would have to be passed.
    """
    x, y = diagram_pos
    ctx.move_to(x, y)
    node_scaling_factor = kwargs.get('device_scaling_factor') * \
        kwargs.get('node_scaling_factor')

    if node_vals is not None:
        for node_row_vals in node_vals:
            colors = plotting.utils.rgb_interpolation(
                node_row_vals, low=low, high=high,
                low_rgb=kwargs.get('low_rgb'), zero_rgb=kwargs.get('zero_rgb'),
                high_rgb=kwargs.get('high_rgb'))
            draw_node_row(ctx, colors, segment_length=segment_length,
                          bit_line_nodes=bit_line,
                          scaling_factor=node_scaling_factor,
                          device=kwargs.get('device_type'))
            y += segment_length
            ctx.move_to(x, y)
    else:
        colors_list = plotting.utils.rgb_single_color(
            crossbar_shape, color=kwargs.get('default_color'))
        for colors in colors_list:
            ctx.move_to(x, y)
            draw_node_row(ctx, colors, bit_line_nodes=bit_line,
                          segment_length=segment_length,
                          scaling_factor=node_scaling_factor,
                          device=kwargs.get('device_type'))
            y += segment_length
            ctx.move_to(x, y)

    ctx.move_to(*diagram_pos)


def dimensions(shape, width_mm=210, color_bar_fraction=(0.5, 0.15),
               border_fraction=0.05):
    """Extracts dimensions of the surface.

    Parameters
    ----------
    shape : tuple of int
        Shape of the crossbar array (`num_word_lines`, `num_bit_lines`).
    max_dim_mm : float, optional
        Width of the diagram in millimeters.
    color_bar_fraction : tuple of float, optional
        The fraction of the surface that the color bar region will take on
        the right (vertically and horizontally.
    border_fraction : float, optional
        Fraction of the `max_dim` that will be blank on all sides of the
        surface.

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
    # convert millimeters to points
    width = width_mm * 72/25.4

    # when plotted, crossbar will take up additional space horizontally
    # and vertically equivalent to half a section dedicated to a single
    # word/bit line
    adjusted_shape = (shape[0]+0.5, shape[1]+0.5)
    # fraction of the horizontal space taken up by the crossbar
    active_horizontal_fraction = 1 - color_bar_fraction[1] - 2 * border_fraction
    # depending on the number of word and bit lines, the larger side of
    # the drawing is determined
    if adjusted_shape[1]/adjusted_shape[0] > active_horizontal_fraction:
        width_fraction = active_horizontal_fraction
        segment_fraction = width_fraction/adjusted_shape[1]
        height_fraction = segment_fraction*adjusted_shape[0]
        height = (height_fraction + 2*border_fraction) * width
        max_dim = width 
    else:
        height_fraction = 1 - 2*border_fraction
        segment_fraction = height_fraction/adjusted_shape[0]
        width_fraction = segment_fraction*adjusted_shape[1]
        height = width / (width_fraction +
                 color_bar_fraction[1] + 2 * border_fraction)
        max_dim = height 

    # if the height is very small compared to the width, additional space
    # is added vertically on both sides
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
