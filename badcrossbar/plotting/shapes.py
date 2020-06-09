import cairo


def line(context, length, angle=0):
    """Draws a line at a specified angle.

    Parameters
    ----------
    context : cairo.Context
        Context.
    length : float
        Length of the line.
    angle : float
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    context.rotate(angle)
    context.rel_line_to(length, 0)
    context.rotate(-angle)
