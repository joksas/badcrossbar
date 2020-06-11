import cairo
import badcrossbar.plotting as plotting


def currents(device_currents, word_line_currents, bit_line_currents,
             default_color=(0, 0, 0), **kwargs):
    device_currents, word_line_currents, bit_line_currents =\
        plotting.utils.average_if_list(
            device_currents, word_line_currents, bit_line_currents)
    crossbar_shape = plotting.utils.arrays_shape(
        device_currents, word_line_currents, bit_line_currents)

    surface_dims, diagram_pos, segment_length, color_bar_pos, color_bar_dims = \
        plotting.crossbar.dimensions(crossbar_shape, max_dim=1000)
    surface = cairo.PDFSurface('crossbar_currents.pdf', *surface_dims)
    context = cairo.Context(surface)

    low, high = plotting.utils.arrays_range(
        device_currents, word_line_currents, bit_line_currents)

    plotting.crossbar.bit_lines(
        context, bit_line_currents, diagram_pos, low, high,
        segment_length=segment_length, default_color=default_color,
        crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.word_lines(
        context, word_line_currents, diagram_pos, low, high,
        segment_length=segment_length, default_color=default_color,
        crossbar_shape=crossbar_shape, **kwargs)

    plotting.crossbar.devices(
        context, device_currents, diagram_pos, low, high,
        segment_length=segment_length, default_color=default_color,
        crossbar_shape=crossbar_shape, **kwargs)

    plotting.color_bar.draw(context, color_bar_pos, color_bar_dims, low, high)
