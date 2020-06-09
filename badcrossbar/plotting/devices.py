import badcrossbar.plotting.shapes as shapes
import numpy as np


def memristor(context, length=140, angle=0):
    """Draws a memristor.

    Parameters
    ----------
    context : cairo.Context
        Context.
    length : float
        Total length of the memristor.
    angle : float
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    unit = length/14
    context.rotate(angle)
    shapes.line(context, 4*unit)
    shapes.line(context, 1.5*unit, -np.pi/2)
    shapes.line(context, 2*unit)
    shapes.line(context, 3*unit, np.pi/2)
    shapes.line(context, 2*unit)
    shapes.line(context, 3*unit, -np.pi/2)
    shapes.line(context, 2*unit)
    shapes.line(context, 1.5*unit, np.pi/2)
    shapes.line(context, 4*unit)
    context.rotate(-angle)
