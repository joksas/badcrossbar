import numpy as np
import numpy.typing as npt
from badcrossbar.computing import kcl
from scipy.sparse import lil_matrix


def g(resistances: npt.NDArray, r_i) -> lil_matrix:
    """Creates and fills matrix `g` used in equation `gv = i`.

    Args:
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Filled matrix `g`.
    """
    if 0 in r_i:
        g_shape = tuple(resistances.size for _ in range(2))
    else:
        g_shape = tuple(2 * resistances.size for _ in range(2))
    g_matrix = lil_matrix(g_shape)
    g_matrix = kcl.apply(g_matrix, resistances, r_i)
    return g_matrix


def i(applied_voltages: npt.NDArray, resistances: npt.NDArray, r_i) -> npt.NDArray:
    """Creates and fills matrix `i` used in equation `gv = i`.

    Values are filled by applying nodal analysis at the leftmost nodes on the
    word lines.

    Args:
        applied_voltages: Applied voltages.
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Filled matrix `i`.
    """
    if 0 in r_i:
        i_shape = (resistances.size, applied_voltages.shape[1])
    else:
        i_shape = (2 * resistances.size, applied_voltages.shape[1])
    i_matrix = np.zeros(i_shape)
    if r_i.word_line > 0:
        i_matrix[: resistances.size : resistances.shape[1], :] = applied_voltages / r_i.word_line
    else:
        i_matrix = np.divide(
            np.repeat(applied_voltages, resistances.shape[1], axis=0),
            np.repeat(resistances.reshape(resistances.size, 1), applied_voltages.shape[1], axis=1),
        )
    return i_matrix
