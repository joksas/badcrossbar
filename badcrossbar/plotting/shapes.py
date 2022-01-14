import cairo
import numpy as np


def line(ctx: cairo.Context, length: float, angle: float = 0):
    """Draws a line at a specified angle.

    Args:
        ctx: Context.
        length: Length of the line.
        angle: Angle in radians of the rotation of plane from the positive x
            axis towards positive y axis.
    """
    ctx.rotate(angle)
    ctx.rel_line_to(length, 0)
    ctx.rotate(-angle)


def semicircle(ctx: cairo.Context, diameter: float, angle: float = 0):
    """Draws a semicircle at a specified angle.

    Args:
        ctx: Context.
        diameter: Diameter of the semicircle.
        angle: Angle in radians of the rotation of plane from the positive x
            axis towards positive y axis.
    """
    ctx.rotate(angle)
    x, y = ctx.get_current_point()
    radius = diameter / 2
    ctx.arc(x + radius, y, radius, np.pi, 2 * np.pi)
    ctx.rotate(-angle)


def rectangle(ctx: cairo.Context, width: float, height: float, angle: float = 0):
    """Draws a rectangle at a specified angle.

    Args:
        ctx: Context.
        width: Width of the rectangle.
        height: Height of the rectangle.
        angle: Angle in radians of the rotation of plane from the positive x
            axis towards positive y axis.
    """
    ctx.rotate(angle)
    x, y = ctx.get_current_point()
    ctx.rectangle(x, y, width, height)
    ctx.rotate(-angle)
