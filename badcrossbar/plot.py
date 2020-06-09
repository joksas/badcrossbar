import cairo
import numpy as np
import badcrossbar.plotting.utils as utils
import badcrossbar.plotting.crossbar as crossbar


def currents(device_currents, word_line_currents, bit_line_currents):
    WIDTH, HEIGHT = 1000, 1000
    surface = cairo.PDFSurface('crossbar_currents.pdf', WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    x_start, y_start = 50, 50
    segment_length = 120
    low, high = utils.arrays_range(
        device_currents, word_line_currents, bit_line_currents)

    x, y = x_start + 1.5*segment_length, y_start + 0.5*segment_length
    ctx.move_to(x, y)

    for bit_line in np.transpose(bit_line_currents):
        colors = utils.rgb_interpolation(bit_line, low=low, high=high)
        crossbar.bit_line(ctx, colors, width=3)
        x += segment_length
        ctx.move_to(x, y)

    x, y = x_start, y_start
    ctx.move_to(x, y)

    for idx, word_line in enumerate(word_line_currents):
        colors = utils.rgb_interpolation(word_line, low=low, high=high)
        if idx == 0:
            crossbar.word_line(ctx, colors, width=3, first=True)
        else:
            crossbar.word_line(ctx, colors, width=3)
        y += segment_length
        ctx.move_to(x, y)

    x, y = x_start, y_start
    ctx.move_to(x, y)
    for device_row in device_currents:
        colors = utils.rgb_interpolation(device_row, low=low, high=high)
        crossbar.device_row(ctx, colors, width=5)

        colors = utils.rgb_interpolation(np.zeros(device_row.shape),
                                         low_rgb=(0, 0, 0))
        ctx.move_to(x, y)
        crossbar.nodes(ctx, colors, diameter=7, bit_line_nodes=True)
        ctx.move_to(x, y)
        crossbar.nodes(ctx, colors, diameter=7, bit_line_nodes=False)
        y += segment_length
        ctx.move_to(x, y)
