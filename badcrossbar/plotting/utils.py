def complete_path(context, rgb=(0, 0, 0), width=1):
    """Completes the current path.

    Parameters
    ----------
    context : cairo.Context
        Context.
    rgb : tuple of int
        Color of the path in RGB (max value of 255 for each).
    width : Width of the path.
    """
    x, y = context.get_current_point()

    context.set_line_width(width)

    rgb = tuple(i/255 for i in rgb)
    context.set_source_rgb(*rgb)

    context.stroke()
    context.move_to(x, y)
