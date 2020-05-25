import numpy as np


def apply(g_matrix, resistances, r_i):
    """Fills matrix g used in equation gv = i.

    Values are filled by applying Kirchhoff's current law at the nodes on the
    word and bit lines.

    Parameters
    ----------
    g_matrix : ndarray
        Matrix g used in equation gv = i.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Filled matrix g.
    """
    with np.errstate(divide='ignore'):
        conductances = 1. / resistances
    g_matrix = word_line_nodes(g_matrix, conductances, r_i)
    g_matrix = bit_line_nodes(g_matrix, conductances, r_i)
    return g_matrix


def word_line_nodes(g_matrix, conductances, r_i):
    """Fills matrix g with values corresponding to nodes on the word lines.

    Parameters
    ----------
    g_matrix : ndarray
        Matrix g used in equation gv = i.
    conductances : ndarray
        Conductances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Partially filled matrix g.
    """
    (num_word_lines, num_bit_lines) = conductances.shape
    g_i = 1 / r_i

    if num_bit_lines != 1:
        # first column
        word_lines = np.arange(num_word_lines)
        bit_lines = np.repeat(0, num_word_lines)
        index = word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones(
            (num_word_lines,))*2*g_i + conductances[:, 0]
        g_matrix[index, index + 1] = -np.ones((num_word_lines,))*g_i
        g_matrix[index, index + conductances.size] = -conductances[:, 0]

        # middle columns
        for i in range(1, num_bit_lines - 1):
            word_lines = np.arange(num_word_lines)
            bit_lines = np.repeat(i, num_word_lines)
            index = word_lines*num_bit_lines + bit_lines
            g_matrix[index, index] = np.ones(
                (num_word_lines,))*2*g_i + conductances[:, i]
            g_matrix[index, index - 1] = -np.ones((num_word_lines,))*g_i
            g_matrix[index, index + 1] = -np.ones((num_word_lines,))*g_i
            g_matrix[index, index + conductances.size] = -conductances[:, i]

        # last column
        word_lines = np.arange(num_word_lines)
        bit_lines = np.repeat(num_bit_lines - 1, num_word_lines)
        index = word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones(
            (num_word_lines,))*g_i + conductances[:, -1]
        g_matrix[index, index - 1] = -np.ones((num_word_lines,))*g_i
        g_matrix[index, index + conductances.size] = -conductances[:, -1]
    else:
        # the only column
        word_lines = np.arange(num_word_lines)
        bit_lines = np.repeat(0, num_word_lines)
        index = word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones(
            (num_word_lines,))*g_i + conductances[:, 0]
        g_matrix[index, index + conductances.size] = -conductances[:, 0]

    return g_matrix


def bit_line_nodes(g_matrix, conductances, r_i):
    """Fills matrix g with values corresponding to nodes on the bit lines.

    Parameters
    ----------
    g_matrix : ndarray
        Matrix g used in equation gv = i.
    conductances : ndarray
        Conductances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Filled matrix g (if this function is executed after word_line_nodes()).
    """
    (num_word_lines, num_bit_lines) = conductances.shape
    g_i = 1 / r_i

    if num_word_lines != 1:
        # first row
        word_lines = np.repeat(0, num_bit_lines)
        bit_lines = np.arange(num_bit_lines)
        index = conductances.size + word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones((num_bit_lines,))*g_i + conductances[
                                                                   0, :]
        g_matrix[index, index + num_bit_lines] = -np.ones(
            (num_bit_lines,))*g_i
        g_matrix[index, index - conductances.size] = -conductances[0, :]

        # middle rows
        for i in range(1, num_word_lines - 1):
            word_lines = np.repeat(i, num_bit_lines)
            bit_lines = np.arange(num_bit_lines)
            index = conductances.size + word_lines*num_bit_lines + bit_lines
            g_matrix[index, index] = np.ones(
                (num_bit_lines,))*2*g_i + conductances[i, :]
            g_matrix[index, index + num_bit_lines] = -np.ones(
                (num_bit_lines,))*g_i
            g_matrix[index, index - num_bit_lines] = -np.ones(
                (num_bit_lines,))*g_i
            g_matrix[index, index - conductances.size] = -conductances[i, :]

        # last row
        word_lines = np.repeat(num_word_lines - 1, num_bit_lines)
        bit_lines = np.arange(num_bit_lines)
        index = conductances.size + word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones(
            (num_bit_lines,))*2*g_i + conductances[-1, :]
        g_matrix[index, index - num_bit_lines] = -np.ones(
            (num_bit_lines,))*g_i
        g_matrix[index, index - conductances.size] = -conductances[-1, :]
    else:
        # the only row
        word_lines = np.repeat(0, num_bit_lines)
        bit_lines = np.arange(num_bit_lines)
        index = conductances.size + word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones((num_bit_lines,))*g_i + conductances[
                                                                   0, :]
        g_matrix[index, index - conductances.size] = -conductances[0, :]

    return g_matrix
