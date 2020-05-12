import numpy as np
from badcrossbar import kcl, display
from scipy.sparse import lil_matrix


def v(voltages, resistances):
    """Fills matrix v with values.

    This function fills matrix v (that will be used to solve matrix equation ri = v) with values.

    :param voltages: Applied voltages.
    :param resistances: Resistances of crossbar devices.
    :return: Filled v matrix.
    """
    v_shape = (3*resistances.size, voltages.shape[1])
    v_matrix = np.zeros(v_shape)
    v_matrix[:resistances.size, :] = np.repeat(voltages, resistances.shape[1], axis=0)
    display.message('v matrix filled.')
    return v_matrix


def g(resistances, r_i):
    if r_i == 0:
        g_shape = tuple(resistances.shape[0] + resistances.shape[1] for _ in range(2))
    else:
        g_shape = tuple(2*resistances.size for _ in range(2))
    g_matrix = np.zeros(g_shape)
    g_matrix = kcl.apply(g_matrix, resistances, r_i)
    return g_matrix


def i(voltages, resistances, r_i):
    if r_i != 0:
        v_shape = (2*resistances.size, voltages.shape[1])
    i_matrix = np.zeros(v_shape)
    i_matrix[:resistances.size:resistances.shape[1], :] = voltages/r_i
    return i_matrix
