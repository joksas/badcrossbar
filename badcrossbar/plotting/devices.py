import badcrossbar.plotting.shapes as shapes
import numpy as np


def memristor(ctx, length=100, angle=0):
    """Draws a memristor.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    length : float
        Total length of the memristor.
    angle : float
        Angle in radians of the rotation of plane from the positive x axis
        towards positive y axis.
    """
    unit = length/14
    ctx.rotate(angle)
    shapes.line(ctx, 4 * unit)
    shapes.line(ctx, 1.5 * unit, -np.pi / 2)
    shapes.line(ctx, 2 * unit)
    shapes.line(ctx, 3 * unit, np.pi / 2)
    shapes.line(ctx, 2 * unit)
    shapes.line(ctx, 3 * unit, -np.pi / 2)
    shapes.line(ctx, 2 * unit)
    shapes.line(ctx, 1.5 * unit, np.pi / 2)
    shapes.line(ctx, 4 * unit)
    ctx.rotate(-angle)
