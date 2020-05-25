from collections import namedtuple
import numpy as np
from badcrossbar import display


def solution(resistances, applied_voltages, **kwargs):
    """Extracts branch currents and node voltages of a crossbar in a
    convenient form.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    applied_voltages : ndarray
        Applied voltages.
    **kwargs
        node_voltages : bool, optional
            If False, None is returned instead of node voltages.

    Returns
    -------
    named tuple
        Branch currents and node voltages of the crossbar.
    """
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = voltages(applied_voltages, resistances)
    extracted_currents = currents(resistances, applied_voltages,
                                  extracted_voltages, **kwargs)
    if kwargs.get('node_voltages', True) is False:
        extracted_voltages = None
    else:
        display.message('Extracted node voltages.', **kwargs)
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def voltages(applied_voltages, resistances):
    """Extracts crossbar node voltages in a convenient format.

    Parameters
    ----------
    applied_voltages : ndarray
        Applied voltages.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    named tuple
        Crossbar node voltages. It has fields 'word_line' and 'bit_line' that
        contain the potentials at the nodes on the word and bit lines.
    """
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])
    word_line_v = word_line_voltages(applied_voltages, resistances)
    bit_line_v = bit_line_voltages(applied_voltages, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    return extracted_voltages


def word_line_voltages(applied_voltages, resistances):
    """Extracts voltages at the nodes on the word lines.

    Parameters
    ----------
    applied_voltages : ndarray
        Applied voltages.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray or list of ndarray
        Voltages at the nodes on the word lines.
    """
    if applied_voltages.shape[1] > 1:
        word_line_v = []
        for i in range(applied_voltages.shape[1]):
            word_line_v.append(
                np.repeat(
                    applied_voltages[:, i:i + 1], resistances.shape[1], axis=1))
    else:
        word_line_v = np.repeat(
            applied_voltages[:, 0:1], resistances.shape[1], axis=1)

    return word_line_v


def bit_line_voltages(applied_voltages, resistances):
    """Extracts voltages at the nodes on the bit lines.

    Parameters
    ----------
    applied_voltages : ndarray
        Applied voltages.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray or list of ndarray
        Voltages at the nodes on the bit lines.
    """
    if applied_voltages.shape[1] > 1:
        bit_line_v = [np.zeros(resistances.shape) for _ in
                      range(applied_voltages.shape[1])]
    else:
        bit_line_v = np.zeros(resistances.shape)

    return bit_line_v


def currents(resistances, applied_voltages, extracted_voltages, **kwargs):
    """Extracts crossbar branch currents in a convenient format.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    applied_voltages : ndarray
        Applied voltages.
    extracted_voltages : ndarray
        Voltages at the nodes of the crossbar.
    **kwargs
        all_currents : bool, optional
            If False, only output currents are returned, while all the other
            ones are set to None.

    Returns
    -------
    named tuple
        Crossbar branch currents. It has fields 'output', 'device', 'word_line'
        and 'bit_line' that contain output currents, as well as currents flowing
        through the devices and interconnect segments of the word and bit lines.
    """
    output_i = output_currents(resistances, applied_voltages)
    device_i = word_line_i = bit_line_i = None

    if kwargs.get('all_currents', True) is False:
        display.message('Extracted output currents.', **kwargs)
    else:
        device_i = device_currents(extracted_voltages.word_line, resistances)
        word_line_i = word_line_currents(resistances, device_i)
        bit_line_i = bit_line_currents(resistances, device_i)
        display.message('Extracted currents from all branches in the '
                        'crossbar.', **kwargs)

    Currents = namedtuple('Currents',
                          ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def output_currents(resistances, applied_voltages):
    """Extracts output currents.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    applied_voltages : ndarray
        Applied voltages.

    Returns
    -------
    ndarray
        Output currents.
    """
    output_i = np.dot(np.transpose(1./resistances), applied_voltages)

    return np.transpose(output_i)


def device_currents(extracted_word_line_voltages, resistances):
    """Extracts currents flowing through crossbar devices.

    Parameters
    ----------
    extracted_word_line_voltages : ndarray or list of ndarray
        Potentials at the nodes on the word lines.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray or list of ndarray
        Currents flowing through crossbar devices.
    """
    if isinstance(extracted_word_line_voltages, list):
        device_i = []
        for w_l in extracted_word_line_voltages:
            device_i.append(np.divide(w_l, resistances))
    else:
        device_i = np.divide(extracted_word_line_voltages, resistances)

    return device_i


def word_line_currents(resistances, device_i_all):
    """Extracts currents flowing through interconnect segments along the word
    lines.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    device_i_all : ndarray
        Currents flowing through crossbar devices.

    Returns
    -------
    ndarray or list of ndarray
        Currents flowing through interconnect segments along the word lines.
    """
    if isinstance(device_i_all, list):
        word_line_i = []
        for device_i in device_i_all:
            temp_word_line_i = np.zeros(resistances.shape)
            temp_word_line_i[:, :] += np.repeat(
                device_i[:, -1:], resistances.shape[1], axis=1)
            for i in range(1, resistances.shape[1]):
                temp_word_line_i[:, :-i] += np.repeat(
                    device_i[:, -(1 + i):-i], resistances.shape[1] - i, axis=1)
            word_line_i.append(temp_word_line_i)
    else:
        word_line_i = np.zeros(resistances.shape)
        word_line_i[:, :] += np.repeat(
            device_i_all[:, -1:], resistances.shape[1], axis=1)
        for i in range(1, resistances.shape[1]):
            word_line_i[:, :-i] += np.repeat(
                device_i_all[:, -(1 + i):-i], resistances.shape[1] - i, axis=1)

    return word_line_i


def bit_line_currents(resistances, device_i_all):
    """Extracts currents flowing through interconnect segments along the bit
    lines.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    device_i_all : ndarray
        Currents flowing through crossbar devices.

    Returns
    -------
    ndarray or list of ndarray
        Currents flowing through interconnect segments along the bit lines.
    """
    if isinstance(device_i_all, list):
        bit_line_i = []
        for device_i in device_i_all:
            temp_bit_line_i = np.zeros(resistances.shape)
            for i in range(resistances.shape[0]):
                temp_bit_line_i[i:, :] += np.repeat(
                    device_i[i:i + 1, :], resistances.shape[0] - i, axis=0)
            bit_line_i.append(temp_bit_line_i)
    else:
        bit_line_i = np.zeros(resistances.shape)
        for i in range(resistances.shape[0]):
            bit_line_i[i:, :] += np.repeat(
                device_i_all[i:i + 1, :], resistances.shape[0] - i, axis=0)

    return bit_line_i
