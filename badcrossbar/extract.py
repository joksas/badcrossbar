import numpy as np
import math
from badcrossbar import display
from collections import namedtuple


def solution(v, resistances, r_i, applied_voltages, shape=(128, 64), **kwargs):
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = None
    if kwargs.get('extract_voltages', True) is True:
        extracted_voltages = voltages(v, resistances, shape=shape)
    extracted_currents = currents(v, resistances, r_i, applied_voltages, shape=shape, **kwargs)
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def currents(v, resistances, r_i, voltages, shape=(128, 64), **kwargs):
    """Extracts crossbar currents in a convenient format.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :param **kwargs:
        :param extract_all: If True, extracts not only the output currents, but also the currents in all the branches of a crossbar.
    :return: Either output currents or output currents together with the currents in all branches.
    """
    output_i = output_currents(v, resistances, r_i, shape)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if kwargs.get('extract_all', True) is False:
        display.message('Extracted output currents.')
    else:
        device_i = device_currents(v, resistances, shape)
        word_line_i = word_line_currents(v, resistances, r_i, voltages, shape)
        bit_line_i = bit_line_currents(v, resistances, r_i, voltages, shape)
        display.message('Extracted currents from all branches in a crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def voltages(v, resistances, shape=(128, 64)):
    """Extracts crossbar currents in a convenient format.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :param **kwargs:
        :param extract_all: If True, extracts not only the output currents, but also the currents in all the branches of a crossbar.
    :return: Either output currents or output currents together with the currents in all branches.
    """
    Voltages = namedtuple('Currents', ['word_line', 'bit_line'])
    word_line_v = word_line_voltages(v, resistances, shape)
    bit_line_v = bit_line_voltages(v, resistances, shape)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    return extracted_voltages


def word_line_voltages(v, resistances, shape):
    v_domain = v[:resistances.size, ]
    return distributed_matrix(v_domain, resistances, shape)


def bit_line_voltages(v, resistances, shape):
    v_domain = v[resistances.size:, ]
    return distributed_matrix(v_domain, resistances, shape)


def output_currents(v, resistances, r_i, shape):
    """Extracts output currents of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: Output currents in a matrix of shape p x n, where p is the number of examples (sets of voltages applied one by one) and n is the number of outputs of the crossbar.
    """
    filled_output_i = v[-resistances.shape[1]:, ]/r_i
    filled_output_i = np.transpose(filled_output_i)
    return filled_output_i


def device_currents(v, resistances, shape):
    """Extracts currents flowing through crossbar devices.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through crossbar devices for each set of applied voltages.
    """
    i = np.divide(v[:resistances.size, ] - v[resistances.size:, ], np.transpose(np.tile(resistances.flatten(), (v.shape[1], 1))))
    return distributed_matrix(i, resistances, shape)


def word_line_currents(v, resistances, r_i, voltages, shape):
    """Extracts currents flowing through interconnects along the word lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through word line interconnects for each set of applied voltages.
    """
    i = np.zeros((resistances.size, shape.voltages[1]))
    i[::resistances.shape[1], ] = (voltages - v[:resistances.size:resistances.shape[1], ].reshape(voltages.shape))/r_i
    for j in range(1, resistances.shape[1]):
        i[j::resistances.shape[1], ] = (v[j-1:resistances.size:resistances.shape[1], ] - v[j:resistances.size:resistances.shape[1], ])/r_i
    return distributed_matrix(i, resistances, shape)


def bit_line_currents(v, resistances, r_i, voltages, shape):
    """Extracts currents flowing through interconnects along the bit lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through bit line interconnects for each set of applied voltages.
    """
    i = np.zeros((resistances.size, shape.voltages[1]))
    for j in range(resistances.shape[0]-1):
        i[resistances.shape[1]*j:resistances.shape[1]*(j+1), ] = (v[resistances.size + resistances.shape[1]*j:resistances.size + resistances.shape[1]*(j+1), ] - v[resistances.size + resistances.shape[1]*(j+1):resistances.size + resistances.shape[1]*(j+2), ])/r_i
    i[-resistances.shape[1]:, ] = v[-resistances.shape[1]:, ]/r_i
    return distributed_matrix(i, resistances, shape)


def distributed_matrix(matrix, resistances, shape):
    """Reshapes flattened vector(s) of currents into an array or a list of arrays.

    :param matrix: A matrix.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: Array or a list of arrays of currents having the same shape as the crossbar.
    """
    if matrix.shape[1] > 1:
        reshaped_i = []
        for example in range(matrix.shape[1]):
            reshaped_matrix = np.zeros(shape.resistances)
            filled_matrix = matrix[:, example].reshape(resistances.shape)
            reshaped_matrix[-filled_matrix.shape[0]:, :filled_matrix.shape[1]] = filled_matrix
            reshaped_i.append(reshaped_matrix)
    else:
        reshaped_i = np.zeros(shape.resistances)
        filled_matrix = matrix.reshape(resistances.shape)
        reshaped_i[-filled_matrix.shape[0]:, :filled_matrix.shape[1]] = filled_matrix

    return reshaped_i


def reduced_resistances(resistances, voltages):
    """If possible, simplifies resistances and voltages matrices.

    If a certain number of word lines at the top or a certain number of bit lines on the right contain insulating devices (those whose resistance is np.inf or math.inf), those word lines and bit lines are removed from the resistances matrix. Solving matrix equation ri = v for reduced r will produce the same results and save computation time.

    :param resistances: Resistances of crossbar devices.
    :param voltages: Applied voltages.
    :return: Resistances and voltages matrices which might have been reduced.
    """
    original_shape = resistances.shape

    # find first row that is non-infinite
    rows = np.where(np.all(resistances == np.inf, axis=1) == False)[0]
    if len(rows) != 0:
        row = rows[0]
        resistances = resistances[row:, :]
        voltages = voltages[row:, :]

    # find last column that is non-infinite
    columns = np.where(np.all(resistances == np.inf, axis=0) == False)[0]
    if len(columns) != 0:
        column = columns[-1]
        resistances = resistances[:, :(column+1)]

    display.reduced(original_shape, resistances.shape)

    return resistances, voltages


def shapes(voltages, resistances):
    """Extracts shapes of voltages and resistances vectors.

    :param voltages: Applied voltages.
    :param resistances: Resistances of crossbar devices.
    :return: Shapes of voltages and resistances matrices.
    """
    Shape = namedtuple('Shape', ['voltages', 'resistances'])
    shape = Shape(voltages.shape, resistances.shape)

    return shape
