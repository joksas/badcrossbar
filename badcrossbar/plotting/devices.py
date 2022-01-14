import badcrossbar.plotting.shapes as shapes
import badcrossbar.plotting.utils as utils
import cairo
import numpy as np


def memristor(
    ctx: cairo.Context,
    length: float = 100,
    angle: float = 0,
    width: float = 1,
    rgb: tuple[float, float, float] = (0, 0, 0),
):
    """Draws a memristor.

    Args:
        ctx: Context.
        length: Total length of the memristor.
        angle: Angle in radians of the rotation of plane from the positive `x`
            axis towards positive `y` axis.
        width: Width of the path.
        rgb: Normalized RGB value of the path.
    """
    unit = length / 14

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

    utils.complete_path(ctx, rgb=rgb, width=width)


def memristor_2(
    ctx: cairo.Context,
    length: float = 100,
    angle: float = 0,
    width: float = 1,
    rgb: tuple[float, float, float] = (0, 0, 0),
):
    """Draws a memristor.

    Replicated from
    <https://commons.wikimedia.org/wiki/File:Memristor-Symbol.svg>

    Args:
        ctx: Context.
        length: Total length of the memristor.
        angle: Angle in radians of the rotation of plane from the positive `x`
            axis towards positive `y` axis.
        width: Width of the path.
        rgb: Normalized RGB value of the path.
    """
    real_width = 2 / 5 * width
    unit = length / 70.866

    ctx.rotate(angle)

    # Outside connector.
    shapes.line(ctx, 17.171 * unit)

    # Wire arranged turning at 90 degree angles.
    shapes.line(ctx, 6.456 * unit)
    ctx.rotate(-np.pi / 2)
    shapes.line(ctx, 3.543 * unit)
    ctx.rotate(np.pi / 2)
    shapes.line(ctx, 6.456 * unit)
    ctx.rotate(np.pi / 2)
    shapes.line(ctx, 7.087 * unit)
    ctx.rotate(-np.pi / 2)
    shapes.line(ctx, 6.456 * unit)
    ctx.rotate(-np.pi / 2)
    shapes.line(ctx, 7.087 * unit)
    ctx.rotate(np.pi / 2)
    shapes.line(ctx, 6.456 * unit)
    ctx.rotate(np.pi / 2)
    shapes.line(ctx, 3.543 * unit)
    ctx.rotate(-np.pi / 2)
    shapes.line(ctx, 6.456 * unit)
    shapes.line(ctx, 4.543 * unit)

    # Rectangle enclosing the wire.
    x, y = ctx.get_current_point()
    ctx.move_to(x, y + 7.5865 * unit)
    ctx.rotate(np.pi / 2)
    shapes.rectangle(ctx, -15.173 * unit, 36.433 * unit)

    utils.complete_path(ctx, rgb=rgb, width=real_width)

    # Filled bottom rectangle.
    x, y = ctx.get_current_point()
    shapes.rectangle(ctx, -15.173 * unit, 4.543 * unit)
    utils.complete_fill(ctx, rgb=rgb)

    # Outside connector.
    x, y = ctx.get_current_point()
    ctx.move_to(x - 7.5865 * unit, y)
    ctx.rotate(-np.pi / 2)
    shapes.line(ctx, 17.717 * unit)
    utils.complete_path(ctx, rgb=rgb, width=real_width)

    ctx.rotate(-angle)


def resistor_usa(
    ctx: cairo.Context,
    length: float = 100,
    angle: float = 0,
    width: float = 1,
    rgb: tuple[float, float, float] = (0, 0, 0),
):
    """Draws a resistor (USA version).

    Args:
        ctx: Context.
        length: Total length of the resistor.
        angle: Angle in radians of the rotation of plane from the positive `x`
            axis towards positive `y` axis.
        width: Width of the path.
        rgb: Normalized RGB value of the path.
    """
    real_width = 3 / 5 * width
    unit = length / 14

    ctx.rotate(angle)
    zigzag_angle = 3 / 8 * np.pi
    zigzag_length = unit / np.cos(zigzag_angle)
    shapes.line(ctx, 4 * unit)
    shapes.line(ctx, 0.5 * zigzag_length, zigzag_angle)
    shapes.line(ctx, zigzag_length, -zigzag_angle)
    shapes.line(ctx, zigzag_length, zigzag_angle)
    shapes.line(ctx, zigzag_length, -zigzag_angle)
    shapes.line(ctx, zigzag_length, zigzag_angle)
    shapes.line(ctx, zigzag_length, -zigzag_angle)
    shapes.line(ctx, 0.5 * zigzag_length, zigzag_angle)
    shapes.line(ctx, 4 * unit)
    ctx.rotate(-angle)

    utils.complete_path(ctx, rgb=rgb, width=real_width)


def resistor_europe(
    ctx: cairo.Context,
    length: float = 100,
    angle: float = 0,
    width: float = 1,
    rgb: tuple[float, float, float] = (0, 0, 0),
):
    """Draws a resistor (European version).

    Args:
        ctx: Context.
        length: Total length of the resistor.
        angle: Angle in radians of the rotation of plane from the positive `x`
            axis towards positive `y` axis.
        width: Width of the path.
        rgb: Normalized RGB value of the path.
    """
    real_width = 3 / 5 * width
    unit = length / 14

    ctx.rotate(angle)
    shapes.line(ctx, 4 * unit)
    ctx.rel_move_to(0, -unit)
    shapes.rectangle(ctx, 6 * unit, 2 * unit)
    ctx.rel_move_to(6 * unit, unit)
    shapes.line(ctx, 4 * unit)
    ctx.rotate(-angle)

    utils.complete_path(ctx, rgb=rgb, width=real_width)
