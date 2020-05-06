import numpy as np


def apply(r, resistances, r_i):
    r = fill_resistances(r, resistances)
    r = fill_horizontal(r, r_i)
    r = fill_vertical(r, r_i)
    return r


def fill_resistances(r, resistances):
    num_resistances = resistances.size
    np.fill_diagonal(r[:num_resistances, :num_resistances], -resistances.flatten())
    return r
