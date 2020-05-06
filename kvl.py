import numpy as np


def apply(r, resistances, r_i):
    r = fill_resistances(r, resistances)
    r = fill_horizontal(r, r_i, resistances)
    r = fill_vertical(r, r_i, resistances)
    return r


def fill_resistances(r, resistances):
    np.fill_diagonal(r[:resistances.size, :resistances.size], -resistances.flatten())
    return r


def fill_horizontal(r, r_i, resistances):
    horizontal = r[:resistances.size, resistances.size:2*resistances.size]
    (num_rows, num_columns) = resistances.shape

    for row in range(num_rows):
        for column in range(num_columns):
            horizontal[row*num_columns+column, row*num_columns:row*num_columns+column+1] = -r_i

    return r


def fill_vertical(r, r_i, resistances):
    vertical = r[:resistances.size, 2*resistances.size:3*resistances.size]
    (num_rows, num_columns) = resistances.shape

    for row in range(num_rows):
        for column in range(num_columns):
            vertical[row*num_columns+column, row*num_columns+column::num_columns] = -r_i

    return r
