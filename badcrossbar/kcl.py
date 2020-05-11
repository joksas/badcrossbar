import numpy as np


def apply(r, resistances):
    """Applies Kirchhoff's current laws to construct part of r matrix.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: r matrix with its second and last thirds of rows filled.
    """
    r = word_line_nodes(r, resistances)
    r = bit_line_nodes(r, resistances)
    return r


def word_line_nodes(r, resistances):
    """Fills r matrix with values corresponding to nodes on the word lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    (num_rows, num_columns) = resistances.shape
    devices_region = r[resistances.size:2*resistances.size, :resistances.size]
    word_lines_region = r[resistances.size:2*resistances.size, resistances.size:2*resistances.size]

    row = np.repeat(np.arange(num_rows), num_columns-1)
    column = np.tile(np.arange(num_columns-1), num_rows)
    word_lines_region[row*num_columns+column, row*num_columns+column] = -1
    word_lines_region[row*num_columns+column, row*num_columns+column+1] = 1
    devices_region[row*num_columns+column, row*num_columns+column] = 1

    # same branches
    row = np.arange(num_columns-1, resistances.size, num_columns)
    column = np.arange(num_columns-1, resistances.size, num_columns)
    word_lines_region[row, column] = -1
    devices_region[row, column] = 1

    r[resistances.size:2 * resistances.size, :resistances.size] = devices_region
    r[resistances.size:2 * resistances.size, resistances.size:2 * resistances.size] = word_lines_region
    return r


def bit_line_nodes(r, resistances):
    """Fills r matrix with values corresponding to nodes on the bit lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Fully filled r matrix (if this function is executed last).
    """
    (num_rows, num_columns) = resistances.shape
    devices_region = r[2*resistances.size:3*resistances.size, :resistances.size]
    bit_lines_region = r[2*resistances.size:3*resistances.size, 2*resistances.size:3*resistances.size]

    row = np.repeat(np.arange(1, num_rows), num_columns)
    column = np.tile(np.arange(num_columns), num_rows-1)
    devices_region[row*num_columns+column, row*num_columns+column] = -1
    bit_lines_region[row*num_columns+column, (row-1)*num_columns+column] = -1
    bit_lines_region[row*num_columns+column, row*num_columns+column] = 1

    # same branches
    row = np.arange(num_columns)
    column = np.arange(num_columns)
    devices_region[row, column] = -1
    bit_lines_region[row, column] = 1

    r[2 * resistances.size:3 * resistances.size, :resistances.size] = devices_region
    r[2 * resistances.size:3 * resistances.size, 2 * resistances.size:3 * resistances.size] = bit_lines_region
    return r
