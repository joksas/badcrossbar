import numpy as np
from badcrossbar import utils
from collections import namedtuple
from badcrossbar.computing import solve


def solution(resistances, r_i, applied_voltages, **kwargs):
    """Extracts branch currents and node voltages of a crossbar in a
    convenient form.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : named tuple of (int or float)
        Interconnect resistances along the word and bit line segments.
    applied_voltages :ndarray
        Applied voltages.
    **kwargs
        node_voltages : bool, optional
            If False, None is returned instead of node voltages.

    Returns
    -------
    named tuple
        Branch currents and node voltages of the crossbar.
    """
    if r_i.word_line == r_i.bit_line == np.inf:
        return insulating_interconnect_solution(
            resistances, applied_voltages, **kwargs)

    v = solve.v(resistances, r_i, applied_voltages, **kwargs)

    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = voltages(v, resistances, **kwargs)
    extracted_currents = currents(
        extracted_voltages, resistances, r_i, applied_voltages, **kwargs)
    if kwargs.get('node_voltages') is not True:
        extracted_voltages = None
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def currents(extracted_voltages, resistances, r_i, applied_voltages, **kwargs):
    """Extracts crossbar branch currents in a convenient format.
    
    Parameters
    ----------
    extracted_voltages : named tuple
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.
    applied_voltages :ndarray
        Applied voltages.
    **kwargs
        all_currents : bool, optional
            If False, only output currents are returned, while all the other
            ones are set to None.

    Returns
    -------
    named tuple
        Crossbar branch currents. Named tuple has fields `output`, `device`,
        `word_line` and `bit_line` that contain output currents, as well as
        currents flowing through the devices and interconnect segments of the
        word and bit lines.
    """
    device_i = device_currents(extracted_voltages, resistances)
    output_i = output_currents(extracted_voltages, device_i, r_i)
    if kwargs.get('all_currents'):
        word_line_i = word_line_currents(
            extracted_voltages, device_i, r_i, applied_voltages)
        bit_line_i = bit_line_currents(
            extracted_voltages, device_i, r_i)
        utils.message(
            'Extracted currents from all branches in the crossbar.', **kwargs)
    else:
        device_i = word_line_i = bit_line_i = None
        utils.message(
            'Extracted output currents.', **kwargs)

    Currents = namedtuple(
        'Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def voltages(v, resistances, **kwargs):
    """Extracts crossbar node voltages in a convenient format.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    named tuple
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    """
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])
    word_line_v = word_line_voltages(v, resistances)
    bit_line_v = bit_line_voltages(v, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    if kwargs.get('node_voltages'):
        utils.message('Extracted node voltages.', **kwargs)
    return extracted_voltages


def word_line_voltages(v, resistances):
    """Extracts voltages at the nodes on the word lines.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray
        Voltages at the nodes on the word lines.
    """
    v_domain = v[:resistances.size, ]
    return utils.distributed_array(v_domain, resistances)


def bit_line_voltages(v, resistances):
    """Extracts voltages at the nodes on the bit lines.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray
        Voltages at the nodes on the bit lines.
    """
    v_domain = v[resistances.size:, ]
    return utils.distributed_array(v_domain, resistances)


def output_currents(extracted_voltages, extracted_device_currents, r_i):
    """Extracts output currents.

    Parameters
    ----------
    extracted_voltages : named tuple
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    extracted_device_currents : ndarray
        Currents flowing through crossbar devices.
    r_i : named tuple of (int or float)
        Interconnect resistances along the word and bit line segments.

    Returns
    -------
    ndarray
        Output currents.
    """
    if r_i.bit_line > 0:
        output_i = extracted_voltages.bit_line[-1, ]/r_i.bit_line
    else:
        output_i = np.sum(extracted_device_currents, axis=0)

    output_i = np.transpose(output_i)
    if output_i.ndim == 1:
        output_i = output_i.reshape(1, output_i.shape[0])
    return output_i


def device_currents(extracted_voltages, resistances):
    """Extracts currents flowing through crossbar devices.

    Parameters
    ----------
    extracted_voltages : named tuple
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray
        Currents flowing through crossbar devices.
    """
    if extracted_voltages.word_line.ndim > 2:
        resistances = np.repeat(resistances[:, :, np.newaxis],
                                extracted_voltages.word_line.shape[2], axis=2)

    v_diff = extracted_voltages.word_line - extracted_voltages.bit_line
    device_i = v_diff/resistances

    return device_i


def word_line_currents(extracted_voltages, extracted_device_currents,
                       r_i, applied_voltages):
    """Extracts currents flowing through interconnect segments along the word
    lines.

    Parameters
    ----------
    extracted_voltages : named tuple
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    extracted_device_currents : ndarray
        Currents flowing through crossbar devices.
    r_i : named tuple of (int or float)
        Interconnect resistances along the word and bit line segments.
    applied_voltages :ndarray
        Applied voltages.

    Returns
    -------
    ndarray
        Currents flowing through interconnect segments along the word lines.
    """
    if r_i.word_line > 0:
        word_line_i = np.zeros(extracted_device_currents.shape)
        if extracted_voltages.word_line.ndim > 2:
            v_diff = applied_voltages - extracted_voltages.word_line[:, 0, ]
            word_line_i[:, 0, ] = v_diff/r_i.word_line
        else:
            v_diff = applied_voltages - extracted_voltages.word_line[:, [0]]
            word_line_i[:, [0]] = v_diff/r_i.word_line

        v_diff = extracted_voltages.word_line[:, :-1, ] - \
            extracted_voltages.word_line[:, 1:, ]
        word_line_i[:, 1:, ] = v_diff/r_i.word_line
    else:
        word_line_i = np.repeat(
            extracted_device_currents[:, -1:, ],
            extracted_device_currents.shape[1], axis=1)
        for i in range(1, extracted_device_currents.shape[1]):
            word_line_i[:, :-i, ] += np.repeat(
                extracted_device_currents[:, -(1 + i):-i, ],
                extracted_device_currents.shape[1]-i, axis=1)

    return word_line_i


def bit_line_currents(extracted_voltages, extracted_device_currents, r_i):
    """Extracts currents flowing through interconnect segments along the bit
    lines.

    Parameters
    ----------
    extracted_voltages : named tuple
        Crossbar node voltages. It has fields `word_line` and `bit_line` that
        contain the potentials at the nodes on the word and bit lines.
    extracted_device_currents : ndarray
        Currents flowing through crossbar devices.
    r_i : named tuple of (int or float)
        Interconnect resistances along the word and bit line segments.

    Returns
    -------
    ndarray
        Currents flowing through interconnect segments along the bit lines.
    """
    if r_i.bit_line > 0:
        bit_line_i = np.zeros(extracted_device_currents.shape)
        v_diff = extracted_voltages.bit_line[:-1, :, ] - \
            extracted_voltages.bit_line[1:, :, ]
        bit_line_i[:-1, :, ] = v_diff/r_i.bit_line
        if extracted_voltages.bit_line.ndim > 2:
            v_diff = extracted_voltages.bit_line[-1, :, ]
            bit_line_i[-1, :, ] = v_diff/r_i.bit_line
        else:
            v_diff = extracted_voltages.bit_line[[-1], :]
            bit_line_i[[-1], :] = v_diff/r_i.bit_line
    else:
        bit_line_i = np.zeros(extracted_device_currents.shape)
        for i in range(extracted_device_currents.shape[0]):
            bit_line_i[i:, :, ] += np.repeat(
                extracted_device_currents[i:i + 1, :, ],
                extracted_device_currents.shape[0] - i, axis=0)

    return bit_line_i


def insulating_interconnect_solution(resistances, applied_voltages, **kwargs):
    """Extracts solution when all interconnects are perfectly insulating.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    applied_voltages : ndarray
        Applied voltages.
    **kwargs
        all_currents : bool, optional
            If False, only output currents are returned, while all the other
            ones are set to None.
        verbose : int
            If 2, makes sure that warning is displayed.

    Returns
    -------
    named tuple
        Branch currents and node voltages of the crossbar.
    """
    if kwargs.get('verbose') == 2:
        kwargs['verbose'] = 1

    Solution = namedtuple('Solution', ['currents', 'voltages'])
    Currents = namedtuple('Currents',
                          ['output', 'device', 'word_line', 'bit_line'])
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])

    extracted_voltages = Voltages(None, None)
    if kwargs.get('node_voltages'):
        utils.message(
            'Warning: all interconnects are perfectly insulating! Node '
            'voltages are undefined!', **kwargs)

    output_i = np.zeros((applied_voltages.shape[1], resistances.shape[1]))
    if kwargs.get('all_currents', True):
        same_i = np.zeros((resistances.shape[0], resistances.shape[1],
                           applied_voltages.shape[1]))
        same_i = utils.squeeze_third_axis(same_i)
        device_i = word_line_i = bit_line_i = same_i
        utils.message(
            'Extracted currents from all branches in the crossbar.', **kwargs)
    else:
        device_i = word_line_i = bit_line_i = None
        utils.message(
            'Extracted output currents.', **kwargs)

    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    extracted_solution = Solution(extracted_currents, extracted_voltages)

    return extracted_solution
