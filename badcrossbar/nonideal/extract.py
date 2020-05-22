import numpy as np
from badcrossbar import display
from collections import namedtuple
from badcrossbar.nonideal import fill, solve


def solution(resistances, r_i, applied_voltages, **kwargs):
    """Extracts currents and voltages in a crossbar in a convenient form.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.
    applied_voltages :ndarray
        Applied voltages.
    kwargs
        node_voltages : bool, optional
            If False, None is returned instead of node voltages.
        all_currents : bool, optional
            If False, only output currents are returned, while all the other ones are set to None.

    Returns
    -------
    named tuple
        Currents and voltages of the crossbar.
    """
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


def currents(v, resistances, r_i, applied_voltages, removed_rows, **kwargs):
    """Extracts crossbar currents in a convenient format.
    
    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.
    applied_voltages :ndarray
        Applied voltages.
    removed_rows : list of int
        Indices of rows removed from g and i.
    kwargs
        all_currents : bool, optional
            If False, only output currents are returned, while all the other ones are set to None.

    Returns
    -------
    named tuple
        Crossbar currents. It has fields 'output', 'device', 'word_line' and 'bit_line' that contain output currents, as well as currents flowing through the devices and interconnect segments of the word and bit lines.
    """
    output_i = output_currents(v, resistances, r_i)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if kwargs.get('all_currents', True) is False:
        display.message('Extracted output currents.')
    else:
        word_line_i = word_line_currents(v, resistances, r_i, applied_voltages)
        bit_line_i = bit_line_currents(v, resistances, r_i)
        device_i = device_currents(v, resistances, removed_rows, word_line_i)

        word_line_i = distributed_array(word_line_i, resistances)
        bit_line_i = distributed_array(bit_line_i, resistances)
        device_i = distributed_array(device_i, resistances)

        display.message('Extracted currents from all branches in the crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def voltages(v, resistances):
    """Extracts crossbar voltages in a convenient format.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    named tuple
        Voltages at the nodes of the crossbar. It has fields 'word_line' and 'bit_line' that contain the potentials at the nodes on the word and bit lines.
    """
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])
    word_line_v = word_line_voltages(v, resistances)
    bit_line_v = bit_line_voltages(v, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    display.message('Extracted node voltages.')
    return extracted_voltages


def word_line_voltages(v, resistances):
    """Extracts potentials at the nodes on the word lines.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray of list of ndarray
        Potentials at the nodes on the word lines.
    """
    v_domain = v[:resistances.size, ]
    return distributed_array(v_domain, resistances)


def bit_line_voltages(v, resistances):
    """Extracts potentials at the nodes on the bit lines.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray of list of ndarray
        Potentials at the nodes on the bit lines.
    """
    v_domain = v[resistances.size:, ]
    return distributed_array(v_domain, resistances)


def output_currents(v, resistances, r_i):
    """Extracts output currents.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Output currents.
    """
    output_i = np.zeros((v.shape[1], resistances.shape[1]))
    filled_output_i = v[-resistances.shape[1]:, ]/r_i
    filled_output_i = np.transpose(filled_output_i)
    output_i[:, :filled_output_i.shape[1]] = filled_output_i
    return output_i


def device_currents(v, resistances, removed_rows, word_line_i):
    """Extracts currents flowing through crossbar devices.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.
    removed_rows : list of int
        Indices of rows removed from g and i.
    word_line_i : ndarray
        Currents flowing through interconnect segments along the word lines.

    Returns
    -------
    ndarray
        Currents flowing through crossbar devices.
    """
    with np.errstate(invalid='ignore'):
        i = np.divide(v[:resistances.size, ] - v[resistances.size:, ], np.transpose(np.tile(resistances.flatten(), (v.shape[1], 1))))
    if removed_rows is not None:
        i = superconductive_device_currents(i, removed_rows, resistances, word_line_i)
    return i


def superconductive_device_currents(device_i, removed_rows, resistances, word_line_i):
    """Extracts currents flowing through crossbar devices that have zero resistance.

    Parameters
    ----------
    device_i : ndarray
        Currents flowing through crossbar devices.
    removed_rows : list of int
        Indices of rows removed from g and i.
    resistances : ndarray
        Resistances of crossbar devices.
    word_line_i : ndarray
        Currents flowing through interconnect segments along the word lines.

    Returns
    -------
    ndarray
        Currents flowing through crossbar devices.
    """
    rows = [x-resistances.size for x in removed_rows]

    for row in rows:
        if (row+1) % resistances.shape[1] == 0:
            device_i[row,] = word_line_i[row]
        else:
            device_i[row,] = word_line_i[row] - word_line_i[row + 1]
    return device_i


def word_line_currents(v, resistances, r_i, applied_voltages):
    """Extracts currents flowing through interconnect segments along the word lines.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.
    applied_voltages :ndarray
        Applied voltages.

    Returns
    -------
    ndarray
        Currents flowing through interconnect segments along the word lines.
    """
    i = np.zeros((resistances.size, applied_voltages.shape[1]))
    i[::resistances.shape[1], ] = (applied_voltages - v[:resistances.size:resistances.shape[1], ]) / r_i
    for j in range(1, resistances.shape[1]):
        i[j::resistances.shape[1], ] = (v[j-1:resistances.size:resistances.shape[1], ] - v[j:resistances.size:resistances.shape[1], ])/r_i
    return i


def bit_line_currents(v, resistances, r_i):
    """Extracts currents flowing through interconnect segments along the bit lines.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Returns
    -------
    ndarray
        Currents flowing through interconnect segments along the bit lines.
    """
    i = np.zeros((resistances.size, v.shape[1]))
    for j in range(resistances.shape[0]-1):
        i[resistances.shape[1]*j:resistances.shape[1]*(j+1), ] = (v[resistances.size + resistances.shape[1]*j:resistances.size + resistances.shape[1]*(j+1), ] - v[resistances.size + resistances.shape[1]*(j+1):resistances.size + resistances.shape[1]*(j+2), ])/r_i
    i[-resistances.shape[1]:, ] = v[-resistances.shape[1]:, ]/r_i
    return i


def distributed_array(flattened_array, model_array):
    """Reshapes flattened array(s) into an array or a list of arrays.
    
    Parameters
    ----------
    flattened_array : ndarray
        An array whose each column contains a flattened array.
    model_array : ndarray
        An array whose shape is used for reshaping.

    Returns
    -------
    ndarray or list of ndarray
        Array or a list of arrays in specified shape.
    """
    if flattened_array.shape[1] > 1:
        reshaped_i = []
        for example in range(flattened_array.shape[1]):
            reshaped_i.append(flattened_array[:, example].reshape(model_array.shape))
    else:
        reshaped_i = flattened_array.reshape(model_array.shape)

    return reshaped_i


def full_v(v, removed_rows, resistances):
    """Refills v with rows that were removed.

    Parameters
    ----------
    v : ndarray
        Solution to gv = i in a flattened form.
    removed_rows : list of int
        Indices of rows removed from g and i.
    resistances : ndarray
        Resistances of crossbar devices.

    Returns
    -------
    ndarray
        Complete v array.
    """
    for row in removed_rows:
        v = np.insert(v, row, 0, axis=0)
        v[row, :] = v[row - resistances.size, :]
    return v


def except_rows(matrix, rows):
    """Deletes certain rows of sparse lil matrix.

    Parameters
    ----------
    matrix : lil_matrix
        Sparse array.
    rows : list of int
        Rows to be removed.

    Returns
    -------
    lil_matrix
        Array with specified rows removed.
    """
    matrix.rows = np.delete(matrix.rows, rows)
    matrix.data = np.delete(matrix.data, rows)
    matrix._shape = (matrix._shape[0] - len(rows), matrix._shape[1])
    return matrix


def except_columns(matrix, columns):
    """Deletes certain columns of sparse lil matrix.

        Parameters
        ----------
        matrix : lil_matrix
            Sparse array.
        columns : list of int
            Columns to be removed.

        Returns
        -------
        lil_matrix
            Array with specified columns removed.
        """
    matrix = except_rows(np.transpose(matrix), columns)
    return np.transpose(matrix)
