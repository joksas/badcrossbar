import numpy as np
from crossbar import kcl, kvl, display
from scipy.sparse import lil_matrix


def r(resistances, r_i):
    """Fills r matrix with values.

    This function goes through all (and slightly more than required) independent loops to perform loop analysis using Kirchhoff's voltage law. Then it identifies current relations using Kirchhoff's current law. In the process, it fills matrix r (that will be used to solve matrix equation ri = v) with values.

    This analysis constructs matrix i so that the first third of its rows corresponds to currents flowing through crossbar devices, the second third corresponds to currents flowing through interconnects along the word lines of the crossbar, and the last third corresponds to currents flowing through interconnects along the bit lines of the crossbar.

    :param resistances: Resistances of crossbar devices.
    :param r_i: Interconnect resistance.
    :return: Filled r matrix.
    """
    r_shape = tuple(3*resistances.size for _ in range(2))
    r_matrix = lil_matrix(r_shape)  # sparse representation to save space; initialised as lil_matrix so that the elements could be easily manipulated before solving
    r_matrix = kvl.apply(r_matrix, resistances, r_i)
    r_matrix = kcl.apply(r_matrix, resistances)
    display.message('r matrix filled.')
    return r_matrix


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
