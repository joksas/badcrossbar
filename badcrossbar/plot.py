import cairo
import numpy as np
import badcrossbar.plotting as plotting


def currents(device_currents, word_line_currents, bit_line_currents):
    device_currents, word_line_currents, bit_line_currents =\
        plotting.utils.average_if_list(
            device_currents, word_line_currents, bit_line_currents)
    crossbar_shape = plotting.utils.arrays_shape(
        device_currents, word_line_currents, bit_line_currents)

    dimensions, pos_start, segment_length, color_bar_dims = \
        plotting.dimensions.get(crossbar_shape, max_dimension=1000)
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
    color_bar(ctx, color_bar_dims, low, high)


def color_bar(context, color_bar_dims, low, high):
    context.rectangle(*color_bar_dims)
    pattern = cairo.LinearGradient(color_bar_dims[0], color_bar_dims[1],
                                   color_bar_dims[0] + color_bar_dims[2],
                                   color_bar_dims[1] + color_bar_dims[3])

    top_rgb = plotting.utils.rgb_interpolation(
        np.array([high]), low=low, high=high)[0]
    if low != high:
        middle_rgb = plotting.utils.rgb_interpolation(
            np.array([0]), low=low, high=high)[0]
    else:
        middle_rgb = plotting.utils.rgb_interpolation(
            np.array([0]), low=-1, high=1)[0]
    bottom_rgb = plotting.utils.rgb_interpolation(
        np.array([low]), low=low, high=high)[0]

    context.set_source_rgb(0, 0, 0)
    font_size = color_bar_dims[2]/2.5
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

    font_size *= 1.5
    context.set_font_size(font_size)
    context.set_source_rgb(0, 0, 0)
    angle = np.pi/2

    _, _, width, height, _, _ = context.text_extents('Current (A)')
    x = color_bar_dims[0] + 2*color_bar_dims[2] + height
    y = color_bar_dims[1] + 0.5*color_bar_dims[3] + 0.5*width
    context.move_to(x, y)

    context.rotate(-angle)
    context.show_text('Current (A)')
    context.rotate(angle)
