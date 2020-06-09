import numpy as np


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


def semicircle(context, diameter, angle=0):
    """Draws a semicircle at a specified angle.

    Parameters
    ----------
    context : cairo.Context
        Context.
    diameter : float
        Diameter of the semicircle.
    angle : float
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    context.rotate(angle)
    x, y = context.get_current_point()
    radius = diameter/2
    context.arc(x+radius, y, radius, np.pi, 2*np.pi)
    context.rotate(-angle)
