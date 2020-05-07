import numpy as np
import kvl
import kcl
from scipy.sparse import lil_matrix


def fill_r(resistances, r_i):
    r_shape = tuple(3*resistances.size for _ in range(2))
    r = lil_matrix(r_shape)
    r = kvl.apply(r, resistances, r_i)
    r = kcl.apply(r, resistances)
    return r


def fill_v(voltages, resistances):
    v_shape = (3*resistances.size, voltages.shape[1])
    v = np.zeros(v_shape)
    v[:resistances.size, :] = np.repeat(voltages, resistances.shape[1], axis=0)
    return v