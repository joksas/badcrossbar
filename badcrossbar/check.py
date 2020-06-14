import numpy as np
from badcrossbar import utils


def crossbar_requirements(resistances, applied_voltages, r_i, **kwargs):
    """Checks if crossbar variables satisfy all requirements.

    Parameters
    ----------
    resistances : any
        Resistances of crossbar devices.
    applied_voltages : any
        Applied voltages.
    r_i : any
        Interconnect resistance.

    Returns
    -------
    ndarray
        Potentially modified (converted to ndarray) resistances and applied
        voltages.
    """
    resistances, applied_voltages = (np.array(i) for i in
                                     (resistances, applied_voltages))
    for i in ((resistances, 2, 'resistances'),
              (applied_voltages, 2, 'applied_voltages')):
        n_dimensional(i[0], i[1], i[2])
        numeric_array(i[0], i[2])
        non_empty(i[0], i[2])

    match_shape(resistances=(resistances, 0),
                applied_voltages=(applied_voltages, 0))
    number(r_i=r_i)
    non_negative_array(resistances, 'resistances')
    negative_number(r_i=r_i)
    short_circuit(resistances, r_i, **kwargs)

    return resistances, applied_voltages


def plotting_requirements(device_currents=None, word_line_currents=None,
                          bit_line_currents=None, word_line_voltages=None,
                          bit_line_voltages=None, currents=True):
    """Checks if arrays containing current values satisfy all requirements.

    Parameters
    ----------
    device_currents : ndarray or None
        Currents flowing through crossbar devices.
    word_line_currents : ndarray or None
        Currents flowing through word line segments.
    bit_line_currents : ndarray or None
        Currents flowing through bit line segments.
    word_line_voltages : ndarray or None
        Voltages at the nodes on the word lines.
    bit_line_voltages : ndarray or None
        Voltages at the nodes on the bit lines.
    currents : bool
        If True, it is assumed that currents are passed. Otherwise, voltages
        are expected.

    Returns
    -------
    ndarray
        Potentially modified (converted to ndarray) currents or voltages.
    """
    if currents:
        valid_arrays = not_none(device_currents=device_currents,
                                word_line_currents=word_line_currents,
                                bit_line_currents=bit_line_currents)
    else:
        valid_arrays = not_none(word_line_voltages=word_line_voltages,
                                bit_line_voltages=bit_line_voltages)
    for key, value in valid_arrays.items():
        valid_arrays[key] = numeric_array(**{key: value})
    empty(**valid_arrays)
    if len(valid_arrays) != 1:
        for dim in [0, 1]:
            dim_arrays = {key: (value, dim)
                          for key, value in valid_arrays.items()}
            match_shape(**dim_arrays)

    if currents:
        return valid_arrays.get('device_currents'), \
            valid_arrays.get('word_line_currents'),\
            valid_arrays.get('bit_line_currents')
    else:
        return valid_arrays.get('word_line_voltages'), \
            valid_arrays.get('bit_line_voltages')


def not_none(**kwargs):
    """Confirms that at least one of the items is not None.

    Parameters
    ----------
    **kwargs : dict of any
        Items of arbitrary type.

    Returns
    -------
    dict of any
        Items that are not None.

    Raises
    -------
    ValueError
        If all of the items are None.
    """
    valid_items = {}
    all_none = True
    for key, value in kwargs.items():
        if value is not None:
            all_none = False
            valid_items[key] = value
    if all_none:
        raise ValueError('At least one of {{{}}} should be not None!'.format(
            ', '.join(kwargs)))

    return valid_items


def number(**kwargs):
    """Confirms that items are int or float.

    Parameters
    ----------
    **kwargs : dict of any
        Items of arbitrary type.

    Raises
    -------
    TypeError
        If any of the items are not int or float.
    """
    for key, value in kwargs.items():
        if not isinstance(value, (int, float)):
            raise TypeError(
                'Type {} of variable \'{}\' is not supported. Use int or '
                'float instead.'.format(type(value).__name__, key))


def n_dimensional(array, n=2, name='array'):
    """Checks that array is n-dimensional.

    Parameters
    ----------
    array : ndarray
        Array.
    n : int
        Required number of dimensions.
    name : str
        Name of the variable.

    Raises
    -------
    TypeError
        If array is not n-dimensional.
    """
    dim = array.ndim
    if dim != n:
        raise TypeError('\'{}\' should be {}-dimensional array! Instead '
                        'received {}-dimensional array.'.format(name, n, dim))


def numeric_array(array, name='array'):
    """Checks that array only contains numbers.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str
        Name of the array.

    Raises
    -------
    TypeError
        If array contains non-number elements.
    """
    if np.issubdtype(array.dtype, np.number) is False:
        raise TypeError('\'{}\' should only contain numbers!'.format(name))


def non_empty(array, name='array'):
    """Checks that array is not empty.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str
        Name of the array.

    Raises
    -------
    ValueError
        If the array is empty.
    """
    if array.size == 0:
        raise ValueError('\'{}\' array is empty!'. format(name))


def match_shape(**kwargs):
    """Checks if arrays have matching dimensions.

    Parameters
    ----------
    **kwargs : dict of tuple of (ndarray and int)
        Arrays and the dimension along which they should be matched.

    Raises
    -------
    ValueError
        If any of the arrays do not match specified dimensions.
    """
    first_key = list(kwargs.keys())[0]
    first_value = list(kwargs.values())[0]
    dim = first_value[0].shape[first_value[1]]
    for key, value in kwargs.items():
        if value[0].shape[value[1]] != dim:
            raise ValueError(
                'Dimension {} of array \'{}\' should match dimension {} of '
                'array \'{}\'!'.format(value[1], key, first_value[1], first_key)
            )


def non_negative_array(array, name='array'):
    """Checks if all the elements of the array are non-negative.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str
        Name of the array.

    Raises
    -------
    ValueError
        If the array contains negative values.
    """
    if (array < 0).any():
        raise ValueError(
            '\'{}\' array contains at least one negative value!'.format(name))


def negative_number(**kwargs):
    """Checks if any of the numbers are negative.

    Parameters
    ----------
    **kwargs : dict of (int or float)
        Numbers.

    Raises
    -------
    ValueError
        If any of the numbers are negative.
    """
    for key, value in kwargs.items():
        if value < 0:
            raise ValueError('Variable \'{}\' is negative!'. format(key))


def short_circuit(resistances, r_i, **kwargs):
    """Checks if crossbar will be short-circuited.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.
    **kwargs
        verbose : int
        If 2, makes sure that warning is displayed.

    Raises
    -------
    ValueError
        If r_i = 0 and any of the devices have zero resistance.
    """

    if 0 in resistances:
        if r_i == 0:
            raise ValueError(
                'At least some crossbar devices have zero resistance causing '
                'short circuit!')
        else:
            if kwargs.get('verbose') == 2:
                kwargs['verbose'] = 1
            utils.message(
                'Warning: some crossbar devices have zero resistance!',
                **kwargs)
