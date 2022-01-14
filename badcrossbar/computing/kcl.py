import numpy as np
import numpy.typing as npt
from scipy.sparse import lil_matrix


def apply(g_matrix: lil_matrix, resistances: npt.NDArray, r_i) -> lil_matrix:
    """Fills matrix `g` used in equation `gv = i`.

    Values are filled by applying Kirchhoff's current law at the nodes on the
    word and bit lines.

    Args:
        g_matrix: Matrix `g` used in equation `gv = i`.
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Filled matrix `g`.
    """
    with np.errstate(divide="ignore"):
        conductances = 1.0 / resistances
    if r_i.word_line > 0:
        g_matrix = word_line_nodes(g_matrix, conductances, r_i)
    if r_i.bit_line > 0:
        g_matrix = bit_line_nodes(g_matrix, conductances, r_i)
    return g_matrix


def word_line_nodes(g_matrix: lil_matrix, conductances: npt.NDArray, r_i) -> lil_matrix:
    """Fills matrix `g` with values corresponding to nodes on the word lines.

    Args:
        g_matrix: Matrix `g` used in equation `gv = i`.
        conductances: Conductances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Partially filled matrix `g`.
    """
    (num_word_lines, num_bit_lines) = conductances.shape
    g_i = 1 / r_i.word_line
    # if `r_i.bit_line == 0`, we are solving only for a half of the matrix
    # `v` and so `bit_line_nodes()` will not even be called.

    if num_bit_lines != 1:
        # first column
        idx_word_lines = np.arange(num_word_lines)
        idx_bit_lines = np.repeat(0, num_word_lines)
        idx = np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
        g_matrix[idx, idx] = np.ones((num_word_lines,)) * 2 * g_i + conductances[:, 0]
        g_matrix[idx, idx + 1] = -np.ones((num_word_lines,)) * g_i
        if r_i.bit_line > 0:
            g_matrix[idx, idx + conductances.size] = -conductances[:, 0]

        # middle columns
        for i in range(1, num_bit_lines - 1):
            idx_word_lines = np.arange(num_word_lines)
            idx_bit_lines = np.repeat(i, num_word_lines)
            idx = np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
            g_matrix[idx, idx] = np.ones((num_word_lines,)) * 2 * g_i + conductances[:, i]
            g_matrix[idx, idx - 1] = -np.ones((num_word_lines,)) * g_i
            g_matrix[idx, idx + 1] = -np.ones((num_word_lines,)) * g_i
            if r_i.bit_line > 0:
                g_matrix[idx, idx + conductances.size] = -conductances[:, i]

        # last column
        idx_word_lines = np.arange(num_word_lines)
        idx_bit_lines = np.repeat(num_bit_lines - 1, num_word_lines)
        idx = np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
        g_matrix[idx, idx] = np.ones((num_word_lines,)) * g_i + conductances[:, -1]
        g_matrix[idx, idx - 1] = -np.ones((num_word_lines,)) * g_i
        if r_i.bit_line > 0:
            g_matrix[idx, idx + conductances.size] = -conductances[:, -1]
    else:
        # the only column
        idx_word_lines = np.arange(num_word_lines)
        idx_bit_lines = np.repeat(0, num_word_lines)
        idx = np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
        g_matrix[idx, idx] = np.ones((num_word_lines,)) * g_i + conductances[:, 0]
        if r_i.bit_line > 0:
            g_matrix[idx, idx + conductances.size] = -conductances[:, 0]

    return g_matrix


def bit_line_nodes(g_matrix: lil_matrix, conductances: npt.NDArray, r_i) -> lil_matrix:
    """Fills matrix g with values corresponding to nodes on the bit lines.

    Args:
        g_matrix: Matrix `g` used in equation `gv = i`.
        conductances: Conductances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Filled matrix `g`.
    """
    (num_word_lines, num_bit_lines) = conductances.shape
    g_bl = 1 / r_i.bit_line
    # if `r_i.word_line == 0`, we are solving only for a half of the matrix
    # `v` and so `word_line_nodes()` will not even be called.
    if r_i.word_line > 0:
        offset = conductances.size
    else:
        offset = 0

    if num_word_lines != 1:
        # first row
        idx_word_lines = np.repeat(0, num_bit_lines)
        idx_bit_lines = np.arange(num_bit_lines)
        idx = offset + np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
        g_matrix[idx, idx] = np.ones((num_bit_lines,)) * g_bl + conductances[0, :]
        g_matrix[idx, idx + num_bit_lines] = -np.ones((num_bit_lines,)) * g_bl
        if r_i.word_line > 0:
            g_matrix[idx, idx - conductances.size] = -conductances[0, :]

        # middle rows
        for i in range(1, num_word_lines - 1):
            idx_word_lines = np.repeat(i, num_bit_lines)
            idx_bit_lines = np.arange(num_bit_lines)
            idx = offset + np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
            g_matrix[idx, idx] = np.ones((num_bit_lines,)) * 2 * g_bl + conductances[i, :]
            g_matrix[idx, idx + num_bit_lines] = -np.ones((num_bit_lines,)) * g_bl
            g_matrix[idx, idx - num_bit_lines] = -np.ones((num_bit_lines,)) * g_bl
            if r_i.word_line > 0:
                g_matrix[idx, idx - conductances.size] = -conductances[i, :]

        # last row
        idx_word_lines = np.repeat(num_word_lines - 1, num_bit_lines)
        idx_bit_lines = np.arange(num_bit_lines)
        idx = offset + np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
        g_matrix[idx, idx] = np.ones((num_bit_lines,)) * 2 * g_bl + conductances[-1, :]
        g_matrix[idx, idx - num_bit_lines] = -np.ones((num_bit_lines,)) * g_bl
        if r_i.word_line > 0:
            g_matrix[idx, idx - conductances.size] = -conductances[-1, :]
    else:
        # the only row
        idx_word_lines = np.repeat(0, num_bit_lines)
        idx_bit_lines = np.arange(num_bit_lines)
        idx = offset + np.ravel_multi_index((idx_word_lines, idx_bit_lines), conductances.shape)
        g_matrix[idx, idx] = np.ones((num_bit_lines,)) * g_bl + conductances[0, :]
        if r_i.word_line > 0:
            g_matrix[idx, idx - conductances.size] = -conductances[0, :]

    return g_matrix
