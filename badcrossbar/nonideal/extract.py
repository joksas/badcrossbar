import numpy as np
from badcrossbar import display
from collections import namedtuple
from badcrossbar.nonideal import fill, solve


def solution(resistances, r_i, applied_voltages, **kwargs):
    g = fill.g(resistances, r_i)
    i = fill.i(applied_voltages, resistances, r_i)
    g, i, removed_rows = fill.superconductive(g, i, resistances, r_i)

    v = solve.v(g, i)
    if removed_rows is not None:
        v = full_v(v, removed_rows, resistances)

    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = None
    if kwargs.get('node_voltages', True) is True:
        extracted_voltages = voltages(v, resistances)
    extracted_currents = currents(v, resistances, r_i, applied_voltages, removed_rows, **kwargs)
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def currents(v, resistances, r_i, voltages, removed_rows, **kwargs):
    """Extracts crossbar currents in a convenient format.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :param **kwargs:
        :param extract_all: If True, extracts not only the output currents, but also the currents in all the branches of a crossbar.
    :return: Either output currents or output currents together with the currents in all branches.
    """
    output_i = output_currents(v, resistances, r_i)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if kwargs.get('all_currents', True) is False:
        display.message('Extracted output currents.')
    else:
        word_line_i = word_line_currents(v, resistances, r_i, voltages)
        bit_line_i = bit_line_currents(v, resistances, r_i)
        device_i = device_currents(v, resistances, removed_rows, word_line_i)

        word_line_i = distributed_matrix(word_line_i, resistances)
        bit_line_i = distributed_matrix(bit_line_i, resistances)
        device_i = distributed_matrix(device_i, resistances)

        display.message('Extracted currents from all branches in the crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def voltages(v, resistances):
    """Extracts crossbar currents in a convenient format.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :param **kwargs:
        :param extract_all: If True, extracts not only the output currents, but also the currents in all the branches of a crossbar.
    :return: Either output currents or output currents together with the currents in all branches.
    """
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])
    word_line_v = word_line_voltages(v, resistances)
    bit_line_v = bit_line_voltages(v, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    display.message('Extracted node voltages.')
    return extracted_voltages


def word_line_voltages(v, resistances):
    v_domain = v[:resistances.size, ]
    return distributed_matrix(v_domain, resistances)


def bit_line_voltages(v, resistances):
    v_domain = v[resistances.size:, ]
    return distributed_matrix(v_domain, resistances)


def output_currents(v, resistances, r_i):
    """Extracts output currents of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: Output currents in a matrix of shape p x n, where p is the number of examples (sets of voltages applied one by one) and n is the number of outputs of the crossbar.
    """
    output_i = np.zeros((v.shape[1], resistances.shape[1]))
    filled_output_i = v[-resistances.shape[1]:, ]/r_i
    filled_output_i = np.transpose(filled_output_i)
    output_i[:, :filled_output_i.shape[1]] = filled_output_i
    return output_i


def device_currents(v, resistances, removed_rows, word_line_i):
    """Extracts currents flowing through crossbar devices.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through crossbar devices for each set of applied voltages.
    """
    with np.errstate(invalid='ignore'):
        i = np.divide(v[:resistances.size, ] - v[resistances.size:, ], np.transpose(np.tile(resistances.flatten(), (v.shape[1], 1))))
    if removed_rows is not None:
        i = superconductive_device_currents(i, removed_rows, resistances, word_line_i)
    return i


def superconductive_device_currents(i, removed_rows, resistances, word_line_i):
    rows = [x-resistances.size for x in removed_rows]

    for row in rows:
        if (row+1) % resistances.shape[1] == 0:
            i[row, ] = word_line_i[row]
        else:
            i[row, ] = word_line_i[row] - word_line_i[row+1]
    return i


def word_line_currents(v, resistances, r_i, voltages):
    """Extracts currents flowing through interconnects along the word lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through word line interconnects for each set of applied voltages.
    """
    i = np.zeros((resistances.size, voltages.shape[1]))
    i[::resistances.shape[1], ] = (voltages - v[:resistances.size:resistances.shape[1], ])/r_i
    for j in range(1, resistances.shape[1]):
        i[j::resistances.shape[1], ] = (v[j-1:resistances.size:resistances.shape[1], ] - v[j:resistances.size:resistances.shape[1], ])/r_i
    return i


def bit_line_currents(v, resistances, r_i):
    """Extracts currents flowing through interconnects along the bit lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through bit line interconnects for each set of applied voltages.
    """
    i = np.zeros((resistances.size, v.shape[1]))
    for j in range(resistances.shape[0]-1):
        i[resistances.shape[1]*j:resistances.shape[1]*(j+1), ] = (v[resistances.size + resistances.shape[1]*j:resistances.size + resistances.shape[1]*(j+1), ] - v[resistances.size + resistances.shape[1]*(j+1):resistances.size + resistances.shape[1]*(j+2), ])/r_i
    i[-resistances.shape[1]:, ] = v[-resistances.shape[1]:, ]/r_i
    return i


def distributed_matrix(matrix, resistances):
    """Reshapes flattened vector(s) of currents into an array or a list of arrays.

    :param matrix: A matrix.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: Array or a list of arrays of currents having the same shape as the crossbar.
    """
    if matrix.shape[1] > 1:
        reshaped_i = []
        for example in range(matrix.shape[1]):
            reshaped_i.append(matrix[:, example].reshape(resistances.shape))
    else:
        reshaped_i = matrix.reshape(resistances.shape)

    return reshaped_i


def full_v(v, removed_rows, resistances):
    for row in removed_rows:
        v = np.insert(v, row, 0, axis=0)
        v[row, :] = v[row - resistances.size, :]
    return v


def except_rows(matrix, rows):
    matrix.rows = np.delete(matrix.rows, rows)
    matrix.data = np.delete(matrix.data, rows)
    matrix._shape = (matrix._shape[0] - len(rows), matrix._shape[1])
    return matrix


def except_columns(matrix, columns):
    matrix = except_rows(np.transpose(matrix), columns)
    return np.transpose(matrix)
