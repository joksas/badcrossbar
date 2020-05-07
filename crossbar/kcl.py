import numpy as np


def apply(r, resistances):
    """Applies Kirchhoff's current laws to construct part of r matrix.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: r matrix with its second and last thirds of rows filled.
    """
    r = fill_left(r, resistances)
    r = fill_right(r, resistances)
    return r


def fill_left(r, resistances):
    """Fills r matrix with values corresponding to nodes on the word lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    (num_rows, num_columns) = resistances.shape
    devices = r[resistances.size:2*resistances.size, :resistances.size]
    horizontal = r[resistances.size:2*resistances.size, resistances.size:2*resistances.size]

    row = np.repeat(np.arange(num_rows), num_columns-1)
    column = np.tile(np.arange(num_columns-1), num_rows)
    horizontal[row*num_columns+column, row*num_columns+column] = -1
    horizontal[row*num_columns+column, row*num_columns+column+1] = 1
    devices[row*num_columns+column, row*num_columns+column] = 1

    # same branches
    row = np.arange(num_columns-1, resistances.size, num_columns)
    column = np.arange(num_columns-1, resistances.size, num_columns)
    horizontal[row, column] = -1
    devices[row, column] = 1

    r[resistances.size:2 * resistances.size, :resistances.size] = devices
    r[resistances.size:2 * resistances.size, resistances.size:2 * resistances.size] = horizontal
    return r


def fill_right(r, resistances):
    """Fills r matrix with values corresponding to nodes on the bit lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Fully filled r matrix (if this function is executed last).
    """
    (num_rows, num_columns) = resistances.shape
    devices = r[2*resistances.size:3*resistances.size, :resistances.size]
    vertical = r[2*resistances.size:3*resistances.size, 2*resistances.size:3*resistances.size]

    row = np.repeat(np.arange(1, num_rows), num_columns)
    column = np.tile(np.arange(num_columns), num_rows-1)
    devices[row*num_columns+column, row*num_columns+column] = -1
    vertical[row*num_columns+column, (row-1)*num_columns+column] = -1
    vertical[row*num_columns+column, row*num_columns+column] = 1

    # same branches
    row = np.arange(num_columns)
    column = np.arange(num_columns)
    devices[row, column] = -1
    vertical[row, column] = 1

    r[2 * resistances.size:3 * resistances.size, :resistances.size] = devices
    r[2 * resistances.size:3 * resistances.size, 2 * resistances.size:3 * resistances.size] = vertical
    return r
