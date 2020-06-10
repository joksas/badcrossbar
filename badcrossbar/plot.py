import cairo
import badcrossbar.plotting as plotting
import badcrossbar.plotting.crossbar


def currents(device_currents, word_line_currents, bit_line_currents):
    device_currents, word_line_currents, bit_line_currents =\
        plotting.utils.average_if_list(
            device_currents, word_line_currents, bit_line_currents)
    crossbar_shape = plotting.utils.arrays_shape(
        device_currents, word_line_currents, bit_line_currents)

    dimensions, pos_start, segment_length, color_bar_dims = \
        badcrossbar.plotting.crossbar.dimensions(crossbar_shape, max_dimension=1000)
    surface = cairo.PDFSurface('crossbar_currents.pdf', *dimensions)
    ctx = cairo.Context(surface)

    low, high = plotting.utils.arrays_range(
        device_currents, word_line_currents, bit_line_currents)

    plotting.crossbar.bit_lines(ctx, bit_line_currents, *pos_start, low, high,
              segment_length=segment_length, crossbar_shape=crossbar_shape)

    plotting.crossbar.word_lines(
        ctx, word_line_currents, *pos_start, low, high,
        segment_length=segment_length, crossbar_shape=crossbar_shape)

    plotting.crossbar.devices(
        ctx, device_currents, *pos_start, low, high,
        segment_length=segment_length, node_color=(0, 0, 0),
        crossbar_shape=crossbar_shape)

    plotting.color_bar.draw(ctx, color_bar_dims, low, high)
