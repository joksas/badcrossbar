import cairo
import badcrossbar.plotting as plotting
import badcrossbar.utils as utils
import badcrossbar.check as check


def currents(device_currents=None, word_line_currents=None,
             bit_line_currents=None, all_currents=None, **kwargs):
    kwargs.setdefault('default_color', (0, 0, 0))
    kwargs.setdefault('wire_scaling_factor', 1)
    kwargs.setdefault('device_scaling_factor', 1)
    kwargs.setdefault('node_scaling_factor', 1)
    kwargs.setdefault('axis_label', 'Current (A)')
    kwargs.setdefault('low_rgb', (213/255, 94/255, 0/255))
    kwargs.setdefault('zero_rgb', (235/255, 235/255, 235/255))
    kwargs.setdefault('high_rgb', (0/255, 114/255, 178/255))
    kwargs.setdefault('allow_overwrite', False)

    if all_currents is not None:
        device_currents = all_currents.device
        word_line_currents = all_currents.word_line
        bit_line_currents = all_currents.bit_line
        device_currents, word_line_currents, bit_line_currents = (
            utils.average_if_3D(i) for i in (
                device_currents, word_line_currents, bit_line_currents))

    device_currents, word_line_currents, bit_line_currents = \
        check.plotting_requirements(
            device_currents=device_currents,
            word_line_currents=word_line_currents,
            bit_line_currents=bit_line_currents, currents=True)

    crossbar_shape = plotting.utils.arrays_shape(
        device_currents, word_line_currents, bit_line_currents)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape, max_dim=1000)
    if kwargs.get('allow_overwrite'):
        filename = 'crossbar-currents.pdf'
    else:
        filename = utils.unique_path('crossbar-currents', 'pdf')
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
    kwargs.setdefault('default_color', (0, 0, 0))
    kwargs.setdefault('wire_scaling_factor', 1)
    kwargs.setdefault('device_scaling_factor', 1)
    kwargs.setdefault('node_scaling_factor', 1.5)
    kwargs.setdefault('axis_label', 'Voltage (V)')
    kwargs.setdefault('low_rgb', (213/255, 94/255, 0/255))
    kwargs.setdefault('zero_rgb', (235/255, 235/255, 235/255))
    kwargs.setdefault('high_rgb', (0/255, 114/255, 178/255))
    kwargs.setdefault('allow_overwrite', False)

    if all_voltages is not None:
        word_line_voltages = all_voltages.word_line
        bit_line_voltages = all_voltages.bit_line
        word_line_voltages, bit_line_voltages = (
            utils.average_if_3D(i) for i in (
                word_line_voltages, bit_line_voltages))

    word_line_voltages, bit_line_voltages = check.plotting_requirements(
        word_line_voltages=word_line_voltages,
        bit_line_voltages=bit_line_voltages, currents=False)

    crossbar_shape = plotting.utils.arrays_shape(word_line_voltages,
                                                 bit_line_voltages)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape, max_dim=1000)
    if kwargs.get('allow_overwrite'):
        filename = 'crossbar-voltages.pdf'
    else:
        filename = utils.unique_path('crossbar-voltages', 'pdf')
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
