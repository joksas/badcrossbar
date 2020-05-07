import numpy as np


def apply(r, resistances, r_i):
    """Applies Kirchhoff's voltage laws to construct part of r matrix.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :param r_i: Interconnect resistance.
    :return: r matrix with its first third of rows filled.
    """
    r = devices(r, resistances)
    if r_i != 0:
        r = word_lines(r, r_i, resistances)
        r = bit_lines(r, r_i, resistances)
    return r


def devices(r, resistances):
    """Fills r matrix with device resistances.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    row = np.arange(resistances.size)
    column = np.arange(resistances.size)
    r[row, column] = resistances.flatten()
    return r


def word_lines(r, r_i, resistances):
    """Fills r matrix with values corresponding to interconnects along word lines.

    :param r: r matrix.
    :param r_i: Interconnect resistance.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    word_lines_region = r[:resistances.size, resistances.size:2*resistances.size]
    (num_rows, num_columns) = resistances.shape

    for row in range(num_rows):
        for column in range(num_columns):
            word_lines_region[row*num_columns+column, row*num_columns:row*num_columns+column+1] = r_i

    r[:resistances.size, resistances.size:2 * resistances.size] = word_lines_region
    return r


def bit_lines(r, r_i, resistances):
    """Fills r matrix with values corresponding to interconnects along bit lines.

    :param r: r matrix.
    :param r_i: Interconnect resistance.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    bit_lines_region = r[:resistances.size, 2*resistances.size:3*resistances.size]
    (num_rows, num_columns) = resistances.shape

    for row in range(num_rows):
        for column in range(num_columns):
            bit_lines_region[row*num_columns+column, row*num_columns+column::num_columns] = r_i

    r[:resistances.size, 2 * resistances.size:3 * resistances.size] = bit_lines_region
    return r
