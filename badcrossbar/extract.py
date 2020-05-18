import numpy as np
from badcrossbar import display
from collections import namedtuple


def solution(v, resistances, r_i, applied_voltages, **kwargs):
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = None
    if kwargs.get('node_voltages', True) is True:
        extracted_voltages = voltages(v, resistances)
    extracted_currents = currents(v, resistances, r_i, applied_voltages, **kwargs)
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def currents(v, resistances, r_i, voltages, **kwargs):
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
        device_i = device_currents(v, resistances)
        word_line_i = word_line_currents(v, resistances, r_i, voltages)
        bit_line_i = bit_line_currents(v, resistances, r_i)
        display.message('Extracted currents from all branches in a crossbar.')

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


def device_currents(v, resistances):
    """Extracts currents flowing through crossbar devices.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param shape: Shape of voltages and resistances matrices.
    :return: List of currents flowing through crossbar devices for each set of applied voltages.
    """
    i = np.divide(v[:resistances.size, ] - v[resistances.size:, ], np.transpose(np.tile(resistances.flatten(), (v.shape[1], 1))))
    return distributed_matrix(i, resistances)


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
    return distributed_matrix(i, resistances)


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
    return distributed_matrix(i, resistances)


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


def zero_solution(resistances, applied_voltages, **kwargs):
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = None
    if kwargs.get('node_voltages', True) is True:
        extracted_voltages = zero_voltages(applied_voltages, resistances)
    extracted_currents = zero_currents(resistances, applied_voltages, extracted_voltages, **kwargs)
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def zero_voltages(applied_voltages, resistances):
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])
    word_line_v = zero_word_line_voltages(applied_voltages, resistances)
    bit_line_v = zero_bit_line_voltages(applied_voltages, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    return extracted_voltages


def zero_word_line_voltages(applied_voltages, resistances):
    if applied_voltages.shape[1] > 1:
        word_line_v = []
        for i in range(applied_voltages.shape[1]):
            word_line_v.append(np.repeat(applied_voltages[:, i:i+1], resistances.shape[1], axis=1))
    else:
        word_line_v = np.repeat(applied_voltages[:, 0:1], resistances.shape[1], axis=1)

    return word_line_v


def zero_bit_line_voltages(applied_voltages, resistances):
    if applied_voltages.shape[1] > 1:
        bit_line_v = [np.zeros(resistances.shape) for _ in range(applied_voltages.shape[1])]
    else:
        bit_line_v = np.zeros(resistances.shape)

    return bit_line_v


def zero_currents(resistances, applied_voltages, extracted_voltages, **kwargs):
    output_i = zero_output_currents(resistances, applied_voltages)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if kwargs.get('all_currents', True) is False:
        display.message('Extracted output currents.')
    else:
        device_i = zero_device_currents(extracted_voltages.word_line, resistances)
        word_line_i = zero_word_line_currents(resistances, device_i)
        bit_line_i = zero_bit_line_currents(resistances, device_i)
        display.message('Extracted currents from all branches in a crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def zero_output_currents(resistances, applied_voltages):
    output_i = np.dot(np.transpose(np.reciprocal(resistances)), applied_voltages)

    return np.transpose(output_i)


def zero_device_currents(extracted_voltages, resistances):
    if isinstance(extracted_voltages, list):
        device_i = []
        for voltages in extracted_voltages:
            device_i.append(np.divide(voltages, resistances))
    else:
        device_i = np.divide(extracted_voltages, resistances)

    return device_i


def zero_word_line_currents(resistances, device_i_all):
    if isinstance(device_i_all, list):
        word_line_i = []
        for device_i in device_i_all:
            temp_word_line_i = np.zeros(resistances.shape)
            temp_word_line_i[:, :] += np.repeat(device_i[:, -1:], resistances.shape[1], axis=1)
            for i in range(1, resistances.shape[1]):
                temp_word_line_i[:, :-i] += np.repeat(device_i[:, -(1+i):-i], resistances.shape[1]-i, axis=1)
            word_line_i.append(temp_word_line_i)
    else:
        word_line_i = np.zeros(resistances.shape)
        word_line_i[:, :] += np.repeat(device_i_all[:, -1:], resistances.shape[1], axis=1)
        for i in range(1, resistances.shape[1]):
            word_line_i[:, :-i] += np.repeat(device_i_all[:, -(1 + i):-i], resistances.shape[1] - i, axis=1)

    return word_line_i


def zero_bit_line_currents(resistances, device_i_all):
    if isinstance(device_i_all, list):
        bit_line_i = []
        for device_i in device_i_all:
            temp_bit_line_i = np.zeros(resistances.shape)
            for i in range(resistances.shape[0]):
                temp_bit_line_i[i:, :] += np.repeat(device_i[i:i+1, :], resistances.shape[0]-i, axis=0)
            bit_line_i.append(temp_bit_line_i)
    else:
        bit_line_i = np.zeros(resistances.shape)
        for i in range(resistances.shape[0]):
            bit_line_i[i:, :] += np.repeat(device_i_all[i:i + 1, :], resistances.shape[0] - i, axis=0)

    return bit_line_i
