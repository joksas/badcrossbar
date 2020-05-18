import numpy as np
from badcrossbar.nonideal import kcl
from scipy.sparse import lil_matrix


def g(resistances, r_i):
    g_shape = tuple(2*resistances.size for _ in range(2))
    g_matrix = lil_matrix(g_shape)
    g_matrix = kcl.apply(g_matrix, resistances, r_i)
    return g_matrix


def i(voltages, resistances, r_i):
    v_shape = (2*resistances.size, voltages.shape[1])
    i_matrix = np.zeros(v_shape)
    i_matrix[:resistances.size:resistances.shape[1], :] = voltages/r_i
    return i_matrix
