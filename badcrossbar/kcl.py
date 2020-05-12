import numpy as np


def apply(g_matrix, resistances, r_i):
    """Fills r matrix with values corresponding to nodes on the word lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    conductances = np.reciprocal(resistances)
    g_matrix = word_line_nodes(g_matrix, conductances, r_i)
    g_matrix = bit_line_nodes(g_matrix, conductances, r_i)
    return g_matrix


def word_line_nodes(g_matrix, conductances, r_i):
    """Fills r matrix with values corresponding to nodes on the word lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Partially filled r matrix.
    """
    (num_word_lines, num_bit_lines) = conductances.shape
    if r_i != 0:
        g_i = 1/r_i

        # first bit line
        word_lines = np.arange(num_word_lines)
        bit_lines = np.repeat(0, num_word_lines)
        index = word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones((num_word_lines,))*2*g_i + conductances[:, 0]
        g_matrix[index, index + 1] = -np.ones((num_word_lines,))*g_i
        g_matrix[index, index + conductances.size] = -conductances[:, 0]

        # middle bit lines
        for i in range(1, num_bit_lines-1):
            word_lines = np.arange(num_word_lines)
            bit_lines = np.repeat(i, num_word_lines)
            index = word_lines * num_bit_lines + bit_lines
            g_matrix[index, index] = np.ones((num_word_lines,))*2*g_i + conductances[:, i]
            g_matrix[index, index - 1] = -np.ones((num_word_lines,))*g_i
            g_matrix[index, index + 1] = -np.ones((num_word_lines,))*g_i
            g_matrix[index, index + conductances.size] = -conductances[:, i]

        # last bit line
        word_lines = np.arange(num_word_lines)
        bit_lines = np.repeat(num_bit_lines-1, num_word_lines)
        index = word_lines * num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones((num_word_lines,))*g_i + conductances[:, -1]
        g_matrix[index, index - 1] = -np.ones((num_word_lines,))*g_i
        g_matrix[index, index + conductances.size] = -conductances[:, -1]

    return g_matrix


def bit_line_nodes(g_matrix, conductances, r_i):
    """Fills r matrix with values corresponding to nodes on the bit lines.

    :param r: r matrix.
    :param resistances: Resistances of crossbar devices.
    :return: Fully filled r matrix (if this function is executed last).
    """
    (num_word_lines, num_bit_lines) = conductances.shape
    if r_i != 0:
        g_i = 1/r_i

        # first word line
        word_lines = np.repeat(0, num_bit_lines)
        bit_lines = np.arange(num_bit_lines)
        index = conductances.size + word_lines*num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones((num_bit_lines,))*g_i + conductances[0, :]
        g_matrix[index, index + num_bit_lines] = -np.ones((num_bit_lines,))*g_i
        g_matrix[index, index - conductances.size] = -conductances[0, :]

        # middle word lines
        for i in range(1, num_word_lines-1):
            word_lines = np.repeat(i, num_bit_lines)
            bit_lines = np.arange(num_bit_lines)
            index = conductances.size + word_lines * num_bit_lines + bit_lines
            g_matrix[index, index] = np.ones((num_bit_lines,))*2*g_i + conductances[i, :]
            g_matrix[index, index + num_bit_lines] = -np.ones((num_bit_lines,))*g_i
            g_matrix[index, index - num_bit_lines] = -np.ones((num_bit_lines,))*g_i
            g_matrix[index, index - conductances.size] = -conductances[i, :]

        # last word line
        word_lines = np.repeat(num_word_lines-1, num_bit_lines)
        bit_lines = np.arange(num_bit_lines)
        index = conductances.size + word_lines * num_bit_lines + bit_lines
        g_matrix[index, index] = np.ones((num_bit_lines,))*g_i + conductances[-1, :]
        g_matrix[index, index - num_bit_lines] = -np.ones((num_bit_lines,))*g_i
        g_matrix[index, index - conductances.size] = -conductances[-1, :]

    return g_matrix
