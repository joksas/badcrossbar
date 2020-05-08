import numpy as np
from crossbar import display
from collections import namedtuple


def currents(i, resistances, extract_all=False):
    """Extracts crossbar currents in a convenient format.

    :param i: Solution to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :param extract_all: If True, extracts not only the output currents, but also the currents in all the branches of a crossbar.
    :return: Either output currents or output currents together with the currents in all branches.
    """
    output_i = output_currents(i, resistances)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if extract_all is False:
        display.message('Extracted output currents.')
    else:
        device_i = device_currents(i, resistances)
        word_line_i = word_line_currents(i, resistances)
        bit_line_i = bit_line_currents(i, resistances)
        display.message('Extracted currents from all branches in a crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def output_currents(i, resistances):
    """Extracts output currents of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :return: Output currents in a matrix of shape p x n, where p is the number of examples (sets of voltages applied one by one) and n is the number of outputs of the crossbar.
    """
    return np.transpose(i[-resistances.shape[1]:, ])


def device_currents(i, resistances):
    """Extracts currents flowing through crossbar devices.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :return: List of currents flowing through crossbar devices for each set of applied voltages.
    """
    i_domain = i[:resistances.size, ]
    return reshaped_currents(i_domain, resistances)


def word_line_currents(i, resistances):
    """Extracts currents flowing through interconnects along the word lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :return: List of currents flowing through word line interconnects for each set of applied voltages.
    """
    i_domain = i[resistances.size:2*resistances.size, ]
    return reshaped_currents(i_domain, resistances)


def bit_line_currents(i, resistances):
    """Extracts currents flowing through interconnects along the bit lines of the crossbar.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :return: List of currents flowing through bit line interconnects for each set of applied voltages.
    """
    i_domain = i[2*resistances.size:3*resistances.size, ]
    return reshaped_currents(i_domain, resistances)


def reshaped_currents(i, resistances):
    """Reshapes flattened vector(s) of currents into an array or a list of arrays.

    :param i: Matrix containing solutions to ri = v in a flattened form.
    :param resistances: Resistances of crossbar devices.
    :return: Array or a list of arrays of currents having the same shape as the crossbar.
    """
    if i.ndim > 1:
        reshaped_i = []
        for example in range(i.shape[1]):
            reshaped_i.append(i[:, example].reshape(resistances.shape))
    else:
        reshaped_i = i.reshape(resistances.shape)

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
