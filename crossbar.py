from scipy.sparse import lil_matrix, csr_matrix
import kvl
import kcl
import numpy as np


def currents(voltages, resistances, r_i=0):
    (num_inputs, num_outputs) = resistances.shape
    num_examples = voltages.shape[1]
    r = fill_r(resistances, r_i)
    v = fill_v(voltages, resistances)
    i = solve(r, v)
    currents = extract_currents(i)

    return currents


def fill_r(resistances, r_i):
    r_shape = tuple(3*resistances.size for _ in range(2))
    r = lil_matrix(r_shape)
    r = kvl.apply(r, resistances, r_i)
    r = kcl.apply(r, resistances)
    return r


def fill_v(voltages, resistances):
    v_shape = (3*resistances.size, voltages.shape[1])
    v = np.zeros(v_shape)
    v[-resistances.size:, :] = np.repeat(voltages, resistances.shape[1], axis=0)
    return v


def solve(r, v):
    i = linalg.spsolve(r.tocsc(), v)
    return i


def extract_currents(i, resistances):
    output_currents = i[-resistances.shape[1]:, ]

    return output_currents
