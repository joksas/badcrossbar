import cairo
from pathvalidate import sanitize_filepath
import badcrossbar.plotting as plotting
import badcrossbar.utils as utils
import badcrossbar.check as check


def currents(device_currents=None, word_line_currents=None,
             bit_line_currents=None, all_currents=None, **kwargs):
    """Produces a diagram of crossbar branch currents and saves it as a PDF
    file.

    If `all_currents` is passed, then it is used to plot the currents.
    Otherwise, one of {`device_currents`, `word_line_currents`,
    `bit_line_currents`} has to be passed.

    Parameters
    ----------
    device_currents : array_like, optional
        Currents flowing through crossbar devices.
    word_line_currents : array_like, optional
        Currents flowing through interconnect segments along the word lines.
    bit_line_currents : array_like, optional
        Currents flowing through interconnect segments along the bit lines.
    all_currents : named tuple, optional
        Crossbar branch currents. Named tuple should have fields `device`,
        `word_line` and `bit_line` that contain currents flowing through the
        devices and interconnect segments of the word and bit lines (at least
        one of them should be not None).

    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the bit lines if their currents are not
            provided.
        wire_scaling_factor : float, optional
            Scaling factor for the width of the word and bit lines.
        device_scaling_factor : float, optional
            Scaling factor for the width of the devices. Also scales the nodes.
        node_scaling_factor : float, optional
            Scaling factor for the diameter of the nodes which is combined
            with `device_scaling_factor`. For example, if one wanted to only
            scale the device width by a factor of 2, but keep the node diameter
            the same, arguments `device_scaling_factor = 2` and
            `node_scaling_factor = 1/2` would have to be passed.
        axis_label : str, optional, optional
            Axis label of the color bar.
        low_rgb : tuple of float, optional
            Normalized RGB value associated with the lower limit.
        zero_rgb : tuple of float, optional
            Normalized RGB value associated with the value of zero.
        high_rgb : tuple of float, optional
            Normalized RGB value associated with the upper limit.
        allow_overwrite : bool, optional
            If True, can overwrite existing PDF files with the same name.
        filename : str, optional
            Filename, excluding PDF extension.
        device : {'memristor', 'resistor_usa', 'resistor_europe'}, optional
            Device type to be drawn.
    """
    kwargs.setdefault('default_color', (0, 0, 0))
    kwargs.setdefault('wire_scaling_factor', 1)
    kwargs.setdefault('device_scaling_factor', 1)
    kwargs.setdefault('node_scaling_factor', 1)
    kwargs.setdefault('axis_label', 'Current (A)')
    kwargs.setdefault('low_rgb', (213/255, 94/255, 0/255))
    kwargs.setdefault('zero_rgb', (235/255, 235/255, 235/255))
    kwargs.setdefault('high_rgb', (0/255, 114/255, 178/255))
    kwargs.setdefault('allow_overwrite', False)
    kwargs.setdefault('filename', 'crossbar-currents')
    kwargs.setdefault('device_type', 'memristor')

    if all_currents is not None:
        device_currents = all_currents.device
        word_line_currents = all_currents.word_line
        bit_line_currents = all_currents.bit_line

    device_currents, word_line_currents, bit_line_currents = \
        check.plotting_requirements(
            device_currents=device_currents,
            word_line_currents=word_line_currents,
            bit_line_currents=bit_line_currents, currents=True)

    crossbar_shape = utils.arrays_shape(
        device_currents, word_line_currents, bit_line_currents)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape, max_dim=1000)
    if kwargs.get('allow_overwrite'):
        filename = '{}.pdf'.format(kwargs.get('filename'))
        filename = sanitize_filepath(filename)
    else:
        filename = utils.unique_path(kwargs.get('filename'), 'pdf')
    surface = cairo.PDFSurface(filename, *surface_dims)
    context = cairo.Context(surface)

    low, high = plotting.utils.arrays_range(
        device_currents, word_line_currents, bit_line_currents)

    plotting.crossbar.bit_lines(
        context, bit_line_currents, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.word_lines(
        context, word_line_currents, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.devices(
        context, device_currents, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    for bit_line in [False, True]:
        plotting.crossbar.nodes(
            context, None, diagram_pos, low, high, bit_line=bit_line,
            segment_length=segment_length, crossbar_shape=crossbar_shape,
            **kwargs)

    plotting.color_bar.draw(context, color_bar_pos, color_bar_dims,
                            low, high, **kwargs)


def voltages(word_line_voltages=None, bit_line_voltages=None,
             all_voltages=None, **kwargs):
    """Produces a diagram of crossbar node voltages and saves it as a PDF file.

    If `all_voltages` is passed, then it is used to plot the voltages.
    Otherwise, one of {`word_line_voltages`, `bit_line_voltages`} has to be
    passed.

    Parameters
    ----------
    word_line_voltages : array_like, optional
        Voltages at the nodes on the word lines.
    bit_line_voltages : array_like, optional
        Voltages at the nodes on the bit lines.
    all_voltages : named tuple, optional
        Crossbar node voltages. It should have fields `word_line` and
        `bit_line` that contain the potentials at the nodes on the word and
        bit lines (at least one of them should be not None).

    **kwargs
        default_color : tuple of float, optional
            Normalized RGB values of the bit lines if their currents are not
            provided.
        wire_scaling_factor : float, optional
            Scaling factor for the width of the word and bit lines.
        device_scaling_factor : float, optional
            Scaling factor for the width of the devices. Also scales the nodes.
        node_scaling_factor : float, optional
            Scaling factor for the diameter of the nodes which is combined
            with `device_scaling_factor`. For example, if one wanted to only
            scale the device width by a factor of 2, but keep the node diameter
            the same, arguments `device_scaling_factor = 2` and
            `node_scaling_factor = 1/2` would have to be passed.
        axis_label : str, optional, optional
            Axis label of the color bar.
        low_rgb : tuple of float, optional
            Normalized RGB value associated with the lower limit.
        zero_rgb : tuple of float, optional
            Normalized RGB value associated with the value of zero.
        high_rgb : tuple of float, optional
            Normalized RGB value associated with the upper limit.
        allow_overwrite : bool, optional
            If True, can overwrite existing PDF files with the same name.
        filename : str, optional
            Filename, excluding PDF extension.
        device : {'memristor', 'resistor_usa', 'resistor_europe'}, optional
            Device type to be drawn.
    """
    kwargs.setdefault('default_color', (0, 0, 0))
    kwargs.setdefault('wire_scaling_factor', 1)
    kwargs.setdefault('device_scaling_factor', 1)
    kwargs.setdefault('node_scaling_factor', 1.4)
    kwargs.setdefault('axis_label', 'Voltage (V)')
    kwargs.setdefault('low_rgb', (213/255, 94/255, 0/255))
    kwargs.setdefault('zero_rgb', (235/255, 235/255, 235/255))
    kwargs.setdefault('high_rgb', (0/255, 114/255, 178/255))
    kwargs.setdefault('allow_overwrite', False)
    kwargs.setdefault('filename', 'crossbar-voltages')
    kwargs.setdefault('device_type', 'memristor')

    if all_voltages is not None:
        word_line_voltages = all_voltages.word_line
        bit_line_voltages = all_voltages.bit_line

    word_line_voltages, bit_line_voltages = check.plotting_requirements(
        word_line_voltages=word_line_voltages,
        bit_line_voltages=bit_line_voltages, currents=False)

    crossbar_shape = utils.arrays_shape(word_line_voltages, bit_line_voltages)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape, max_dim=1000)
    if kwargs.get('allow_overwrite'):
        filename = '{}.pdf'.format(kwargs.get('filename'))
        filename = sanitize_filepath(filename)
    else:
        filename = utils.unique_path(kwargs.get('filename'), 'pdf')
    surface = cairo.PDFSurface(filename, *surface_dims)
    context = cairo.Context(surface)

    low, high = plotting.utils.arrays_range(word_line_voltages,
                                            bit_line_voltages)

    plotting.crossbar.bit_lines(
        context, None, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.word_lines(
        context, None, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.devices(
        context, None, diagram_pos, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape, **kwargs)

    for node_voltages, bit_line in zip([word_line_voltages, bit_line_voltages],
                                       [False, True]):
        plotting.crossbar.nodes(
            context, node_voltages, diagram_pos, low, high, bit_line=bit_line,
            segment_length=segment_length, crossbar_shape=crossbar_shape,
            **kwargs)

    plotting.color_bar.draw(context, color_bar_pos, color_bar_dims,
                            low, high, **kwargs)
