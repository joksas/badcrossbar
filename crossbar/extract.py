import numpy as np
import math
from crossbar import display
from collections import namedtuple


def currents(i, resistances, shape=(128, 64), **kwargs):
    """Extracts crossbar currents in a convenient format.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :param **kwargs:
        :param extract_all: If True, extracts not only the output currents, but also the currents in all the branches of a crossbar.
    :return: Either output currents or output currents together with the currents in all branches.
    """
    i = rounded_zeros_i(i, resistances, part='first')
    output_i = output_currents(i, resistances, shape)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if kwargs.get('extract_all', True) is False:
        display.message('Extracted output currents.')
    else:
        i = rounded_zeros_i(i, resistances, part='rest')
        device_i = device_currents(i, resistances, shape)
        word_line_i = word_line_currents(i, resistances, shape)
        bit_line_i = bit_line_currents(i, resistances, shape)
        display.message('Extracted currents from all branches in a crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def output_currents(i, resistances, shape):
    """Extracts output currents of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: Output currents in a matrix of shape p x n, where p is the number of examples (sets of voltages applied one by one) and n is the number of outputs of the crossbar.
    """
    output_i = np.zeros((shape.voltages[1], shape.resistances[1]))
    filled_output_i = np.transpose(i[-resistances.shape[1]:, ])
    if filled_output_i.ndim > 1:
        output_i[:, :filled_output_i.shape[1]] = filled_output_i
    else:
        output_i[:, :filled_output_i.shape[0]] = filled_output_i
    return output_i


def device_currents(i, resistances, shape):
    """Extracts currents flowing through crossbar devices.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through crossbar devices for each set of applied voltages.
    """
    i_domain = i[:resistances.size, ]
    return reshaped_currents(i_domain, resistances, shape)


def word_line_currents(i, resistances, shape):
    """Extracts currents flowing through interconnects along the word lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through word line interconnects for each set of applied voltages.
    """
    i_domain = i[resistances.size:2*resistances.size, ]
    return reshaped_currents(i_domain, resistances, shape)


def bit_line_currents(i, resistances, shape):
    """Extracts currents flowing through interconnects along the bit lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through bit line interconnects for each set of applied voltages.
    """
    i_domain = i[2*resistances.size:3*resistances.size, ]
    return reshaped_currents(i_domain, resistances, shape)


def reshaped_currents(i, resistances, shape):
    """Reshapes flattened vector(s) of currents into an array or a list of arrays.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: Array or a list of arrays of currents having the same shape as the crossbar.
    """
    if i.ndim > 1:
        reshaped_i = []
        for example in range(i.shape[1]):
            reshaped_matrix = np.zeros(shape.resistances)
            filled_matrix = i[:, example].reshape(resistances.shape)
            reshaped_matrix[-filled_matrix.shape[0]:, :filled_matrix.shape[1]] = filled_matrix
            reshaped_i.append(reshaped_matrix)
    else:
        reshaped_i = np.zeros(shape.resistances)
        filled_matrix = i.reshape(resistances.shape)
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
    rows = np.where(np.all(resistances > large_number(), axis=1) == False)[0]
    if len(rows) != 0:
        row = rows[0]
        resistances = resistances[row:, :]
        voltages = voltages[row:, :]

    # find last column that is non-infinite
    columns = np.where(np.all(resistances > large_number(), axis=0) == False)[0]
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


def non_infinite(matrix):
    """Replaces np.inf values with very large numbers.

    In most cases, this function would not be necessary to solve matrix equations. Unfortunately, in a few edge cases, even when there is an analytic solution, scipy library is not able to compute i matrix when some specific r entries are equal to np.inf. Replacing np.inf with very large numbers seems to provide a stable solution (see tests directory).

    :param matrix: An array.
    :return: An array in which np.inf values are replaced with a very large number.
    """
    matrix[matrix == np.inf] = large_number()
    return matrix


def large_number():
    """Return large number.

    :return: Large number.
    """
    return 1e200


def rounded_zeros(matrix):
    """Rounds numbers with very small absolute values to zero.

    This function was mainly created to deal with very small crossbar currents that should, in theory, be zero but are computed as non-zero because of extract.non_infinite().

    :param matrix: A numpy array.
    :return: A numpy array with its smallest absolute values set to zero.
    """
    order_of_magnitude = np.floor(math.log(large_number(), 10))
    threshold = 1/(10 ** int(order_of_magnitude*0.9))

    almost_zero = np.where((matrix > -threshold) & (matrix < threshold))
    matrix[almost_zero] = 0

    return matrix


def rounded_zeros_i(i, resistances, part='whole'):
    """Rounds numbers in i matrix with very small absolute values to zero.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param part: Subset of currents that has to be rounded.
    :return: i matrix with some or all of its small values rounded to zero.
    """
    if part == 'output':
        i[-resistances.shape[1]:, ] = rounded_zeros(i[-resistances.shape[1]:, ])
    elif part == 'rest':
        i[:resistances.shape[1], ] = rounded_zeros(i[:resistances.shape[1], ])
    elif part == 'whole':
        i = rounded_zeros(i)

    return i
