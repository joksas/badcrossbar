import numpy as np


def line(ctx, length, angle=0):
    """Draws a line at a specified angle.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    length : float
        Length of the line.
    angle : float, optional
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    ctx.rotate(angle)
    ctx.rel_line_to(length, 0)
    ctx.rotate(-angle)


def semicircle(ctx, diameter, angle=0):
    """Draws a semicircle at a specified angle.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    diameter : float
        Diameter of the semicircle.
    angle : float, optional
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    ctx.rotate(angle)
    x, y = ctx.get_current_point()
    radius = diameter/2
    ctx.arc(x + radius, y, radius, np.pi, 2 * np.pi)
    ctx.rotate(-angle)


def rectangle(ctx, width, height, angle=0):
    """Draws a rectangle at a specified angle.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    width : float
        Width of the rectangle.
    height : float
        Height of the rectangle.
    angle : float, optional
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    ctx.rotate(angle)
    x, y = ctx.get_current_point()
    ctx.rectangle(x, y, width, height)
    ctx.rotate(-angle)

