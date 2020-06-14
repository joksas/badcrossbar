import numpy as np
from collections import namedtuple
from badcrossbar import utils

Solution = namedtuple('Solution', ['currents', 'voltages'])
Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])


def qucs_dat_file(filename, shape):
    """Extracts setup and solution associated with a Qucs data file.

    For a particular circuit defined in Qucs, the user can select to
    "Calculate DC bias"; this generates a DAT file, containing the simulation
    setup, as well as currents flowing though ammeters and voltages at named
    nodes. This function extracts this information, transforms it into
    convenient form and saves it as a pickle file.

    Parameters
    ----------
    filename : str
        Name of the DAT file, excluding extension.
    shape : tuple of int
        Shape of the crossbar array (`num_word_lines`, `num_bit_lines`).
    """
    data = open_file(filename, 'dat')
    R = two_dim(data, shape, var1='R')
    V = one_dim(data, shape, var1='V')
    r_i = zero_dim(data, var1='r_i')
    I_o, I_d, I_w, I_b, V_w, V_b = solution(data, shape)
    utils.save_pickle((R, V, r_i, I_o, I_d, I_w, I_b, V_w, V_b), filename,
                      allow_overwrite=True)


def two_dim(data, shape, var1, var2=None):
    """Extracts 2D array from Qucs DAT file.

    This only works if the user uses two indices for naming.

    Parameters
    ----------
    data : str
        Contents of the DAT file.
    shape : tuple of int
        Shape of the crossbar array (`num_word_lines`, `num_bit_lines`).
    var1 :str
        Name of the first variable.
    var2 : str, optional
        Name of the second variable.

    Returns
    -------
    ndarray
        2D Array.
    """
    X = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            delim1 = '<indep ' + var1 + str(i) + str(j)
            if var2 is not None:
                delim1 += var2
            delim1 += ' 1>\n'
            delim2 = '\n</indep>'
            text = between(data, delim1, delim2)
            X[i, j] = float(text)

    return X


def one_dim(data, shape, var1, var2=None):
    """Extracts 1D array from Qucs DAT file.

    Parameters
    ----------
    data : str
        Contents of the DAT file.
    shape : tuple of int
        Shape of the crossbar array (`num_word_lines`, `num_bit_lines`).
    var1 :str
        Name of the first variable.
    var2 : str, optional
        Name of the second variable.

    Returns
    -------
    ndarray
        2D Array.
    """
    X = np.zeros((shape[0], 1))
    for i in range(shape[0]):
        delim1 = '<indep ' + var1 + str(i)
        if var2 is not None:
            delim1 += var2
        delim1 += ' 1>\n'
        delim2 = '\n</indep>'
        text = between(data, delim1, delim2)
        X[i, 0] = float(text)

    return X


def zero_dim(data, var1, var2=None):
    """Extracts a scalar from Qucs DAT file.

    Parameters
    ----------
    data : str
        Contents of the DAT file.
    var1 :str
        Name of the first variable.
    var2 : str, optional
        Name of the second variable.

    Returns
    -------
    int or float
        A scalar.
    """
    delim1 = '<indep ' + var1
    if var2 is not None:
        delim1 += var2
    delim1 += ' 1>\n'
    delim2 = '\n</indep>'
    text = between(data, delim1, delim2)
    return float(text)


def solution(data, shape):
    """Extracts solution from Qucs DAT file.

    Parameters
    ----------
    data : str
        Contents of the DAT file.
    shape : tuple of int
        Shape of the crossbar array (`num_word_lines`, `num_bit_lines`).

    Returns
    -------
    ndarray
        Branch currents and node voltages of the crossbar array.
    """
    device_currents = two_dim(data, shape, var1='d', var2='.I')
    word_line_currents = two_dim(data, shape, var1='w', var2='.I')
    bit_line_currents = two_dim(data, shape, var1='b', var2='.I')
    output_currents = bit_line_currents[-1, :].reshape(1, shape[1])

    word_line_voltages = two_dim(data, shape, var1='w', var2='.V')
    bit_line_voltages = two_dim(data, shape, var1='b', var2='.V')

    return output_currents, device_currents, word_line_currents, \
           bit_line_currents, word_line_voltages, bit_line_voltages


def between(data, delim1, delim2):
    """Extracts text between two delimiters.

    Parameters
    ----------
    data : str
        Text to analyse
    delim1 : str
        First delimiter.
    delim2 : str
        Second delimiter.

    Returns
    -------
    str
        Text between delimiters.
    """
    return data.split(delim1)[1].split(delim2)[0]


def open_file(filename, extension):
    """Loads arbitrary file.

    Parameters
    ----------
    filename : str
        Name of the file, excluding extension.
    extension : str
        File extension.

    Returns
    -------
    any
        Contents of the file.
    """
    with open(filename + '.' + extension, 'r') as opened_file:
        contents = opened_file.read()
    return contents
