from scipy.sparse import linalg
from badcrossbar import utils
from badcrossbar.computing import fill
import numpy as np


def v(resistances, r_i, applied_voltages, **kwargs):
    """Solves matrix equation gv = i.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : named tuple of (int or float)
        Interconnect resistances along the word and bit line segments.
    applied_voltages :ndarray
        Applied voltages.

    Returns
    -------
    ndarray
        Matrix containing potentials at each of the nodes.
    """
    if r_i.word_line > 0 or r_i.bit_line > 0:
        g = fill.g(resistances, r_i)
        i = fill.i(applied_voltages, resistances, r_i)

        utils.message('Started solving for v.', **kwargs)
        v_matrix = linalg.spsolve(g.tocsc(), i)
        utils.message('Solved for v.', **kwargs)

        if v_matrix.ndim == 1:
            v_matrix = v_matrix.reshape(v_matrix.shape[0], 1)

        if r_i.word_line == 0:
            new_v_matrix = np.zeros(
                (2*resistances.size, applied_voltages.shape[1]))
            new_v_matrix[:resistances.size, ] = np.repeat(
                applied_voltages, resistances.shape[1], axis=0)
            new_v_matrix[resistances.size:, ] = v_matrix
            v_matrix = new_v_matrix
        if r_i.bit_line == 0:
            new_v_matrix = np.zeros(
                (2*resistances.size, applied_voltages.shape[1]))
            new_v_matrix[:resistances.size, ] = v_matrix
            v_matrix = new_v_matrix
    else:
        v_matrix = np.zeros(
                (2*resistances.size, applied_voltages.shape[1]))
        v_matrix[:resistances.size, ] = np.repeat(
                applied_voltages, resistances.shape[1], axis=0)

    return v_matrix
