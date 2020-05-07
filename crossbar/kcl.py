import numpy as np


def apply(r, resistances):
    r = fill_left(r, resistances)
    r = fill_right(r, resistances)
    return r


def fill_left(r, resistances):
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