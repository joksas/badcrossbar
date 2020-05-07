import numpy as np
from crossbar import kcl, kvl, display
from scipy.sparse import lil_matrix


def r(resistances, r_i):
    r_shape = tuple(3*resistances.size for _ in range(2))
    r_matrix = lil_matrix(r_shape)
    r_matrix = kvl.apply(r_matrix, resistances, r_i)
    r_matrix = kcl.apply(r_matrix, resistances)
    display.message('r matrix filled.')
    return r_matrix


def v(voltages, resistances):
    v_shape = (3*resistances.size, voltages.shape[1])
    v_matrix = np.zeros(v_shape)
    v_matrix[:resistances.size, :] = np.repeat(voltages, resistances.shape[1], axis=0)
    display.message('v matrix filled.')
    return v_matrix
