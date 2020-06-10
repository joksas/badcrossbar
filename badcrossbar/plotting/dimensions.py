import badcrossbar.plotting as plotting


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


