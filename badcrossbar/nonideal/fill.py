import numpy as np
from badcrossbar.nonideal import kcl
from scipy.sparse import lil_matrix
from badcrossbar.nonideal import extract


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


def superconductive(g_matrix, i_matrix, resistances, r_i):
    # get rows of g_matrix that contain np.inf elements
    rows = np.argwhere(np.any(g_matrix[:resistances.size, :] == np.inf, axis=0) == True)[:, -1]
    if len(rows) == 0:
        return g_matrix, i_matrix, None

    g_matrix[g_matrix == np.inf] = 0
    g_matrix[g_matrix == -np.inf] = 0

    for row in rows:
        g_matrix[row, :] += g_matrix[row + resistances.size, :]
        g_matrix[:, row] += g_matrix[:, row + resistances.size]

    removed_rows = list(map(int, rows + np.ones(rows.shape)*resistances.size))
    g_matrix = extract.delete_rows(g_matrix, removed_rows)
    g_matrix = extract.delete_columns(g_matrix, removed_rows)
    i_matrix = np.delete(i_matrix, removed_rows, 0)

    for row in rows:
        g_matrix[row, row] = -np.sum(g_matrix[row, :])
        if row % resistances.shape[1] == 0:
            g_matrix[row, row] += 1/r_i
        if resistances.size - row <= resistances.shape[1]:
            g_matrix[row, row] += 1 / r_i

    return g_matrix, i_matrix, removed_rows
