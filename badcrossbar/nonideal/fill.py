import numpy as np
from badcrossbar.nonideal import kcl
from scipy.sparse import lil_matrix
from badcrossbar.nonideal import extract


def g(resistances, r_i):
    """Creates and fills matrix g used in equation gv = i.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Filled matrix g.
    """
    g_shape = tuple(2*resistances.size for _ in range(2))
    g_matrix = lil_matrix(g_shape)
    g_matrix = kcl.apply(g_matrix, resistances, r_i)
    return g_matrix


def i(applied_voltages, resistances, r_i):
    """Creates and fills matrix i used in equation gv = i.

    Values are filled by applying nodal analysis at the leftmost nodes on the
    word lines.

    Parameters
    ----------
    applied_voltages :ndarray
        Applied voltages.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Filled matrix i.
    """
    v_shape = (2*resistances.size, applied_voltages.shape[1])
    i_matrix = np.zeros(v_shape)
    i_matrix[:resistances.size:resistances.shape[1], :] = applied_voltages/r_i
    return i_matrix


def superconductive(g_matrix, i_matrix, resistances, r_i):
    """Transforms matrices g and i (used in equation gv = i) so that the
    equation could be solved even if some of the crossbar devices have zero
    resistance.

    When some crossbar devices have zero resistance, g() can yield a singular
    matrix. To avoid that, redundant nodes (those next to devices with zero
    resistance) have to removed before attempting to solve. In this function,
    nodes on the bit lines next to devices with zero resistance are removed.
    Any references from and to those nodes are now encoded into descriptions
    of corresponding nodes on the word lines because they share the same
    potential.

    Parameters
    ----------
    g_matrix : ndarray
        matrix g used in equation gv = i
    i_matrix : ndarray
        matrix i used in equation gv = i
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    g_matrix, i_matrix : ndarray
        Transformed matrices g and i (used in equation gv = i).
    removed_rows : list of int
        Indices of removed rows from the two matrices.
    """
    # get rows, corresponding to equations set for nodes on the word line,
    # of g_matrix that contain np.inf elements
    rows = np.argwhere(
        np.any(g_matrix[:resistances.size, :] == np.inf, axis=0) == True)[:, -1]
    if len(rows) == 0:
        return g_matrix, i_matrix, None

    g_matrix[g_matrix == np.inf] = g_matrix[g_matrix == -np.inf] = 0

    for row in rows:
        # add nodes referenced by bit line node to the list of nodes that
        # word line node references
        g_matrix[row, :] += g_matrix[row + resistances.size, :]
        # redirect references, that were directed to the bit line node,
        # to word line node
        g_matrix[:, row] += g_matrix[:, row + resistances.size]

    # transform matrices by removing redundant bit line nodes
    removed_rows = list(map(int, rows + np.ones(rows.shape)*resistances.size))
    g_matrix = extract.except_rows(g_matrix, removed_rows)
    g_matrix = extract.except_columns(g_matrix, removed_rows)
    i_matrix = np.delete(i_matrix, removed_rows, 0)

    # some of the information was lost in function g() when np.inf elements
    # were added
    # to matrix g and overrode any existing values; these steps recover that
    # information
    for row in rows:
        g_matrix[row, row] = -np.sum(g_matrix[row, :])
        if row % resistances.shape[1] == 0:
            g_matrix[row, row] += 1/r_i
        if resistances.size - row <= resistances.shape[1]:
            g_matrix[row, row] += 1/r_i

    return g_matrix, i_matrix, removed_rows
