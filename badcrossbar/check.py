import numpy as np
from badcrossbar import display


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
    resistances, applied_voltages = matrix_type(
        resistances=resistances, applied_voltages=applied_voltages)
    empty(resistances=resistances, applied_voltages=applied_voltages)
    match_shape(resistances=(resistances, 0),
                applied_voltages=(applied_voltages, 0))
    number(r_i=r_i)
    negative_array(resistances=resistances)
    negative_number(r_i=r_i)
    short_circuit(resistances, r_i, **kwargs)

    return resistances, applied_voltages


def current_plotting_requirements(device_currents, word_line_currents,
                                  bit_line_currents):
    """Checks if arrays containing current values satisfy all requirements.

    Parameters
    ----------
    device_currents : ndarray or None
        Currents flowing through crossbar devices.
    word_line_currents : ndarray or None
        Currents flowing through word line segments.
    bit_line_currents : ndarray or None
        Currents flowing through bit line segments.

    Returns
    -------
    ndarray
        Potentially modified (converted to ndarray) currents.
    """
    valid_arrays = not_none(device_currents=device_currents,
                            word_line_currents=word_line_currents,
                            bit_line_currents=bit_line_currents)
    for key, value in valid_arrays.items():
        valid_arrays[key] = matrix_type(**{key: value})
    empty(**valid_arrays)
    if len(valid_arrays) != 1:
        for dim in [0, 1]:
            dim_arrays = {key: (value, dim)
                          for key, value in valid_arrays.items()}
            match_shape(**dim_arrays)

    return valid_arrays.get('device_currents'), \
        valid_arrays.get('word_line_currents'),\
        valid_arrays.get('bit_line_currents')


def not_none(**kwargs):
    """Confirms that at least one of the items is not None.

    Parameters
    ----------
    kwargs : any
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
    kwargs : any
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


def matrix_type(**kwargs):
    """Checks if items can be used as numpy arrays.

    If one of the arguments is already a numpy array, it is returned
    unchanged. If it is a list of lists, it is converted to numpy array and
    then returned. Else, an error is raised.

    Parameters
    ----------
    kwargs : any
        Items of arbitrary type.

    Returns
    -------
    list of ndarray

    Raises
    -------
    TypeError
        If any of the items are not ndarray or list, or if they contain
        non-number elements.
    """
    new_args = []
    good_type = True
    for key, value in kwargs.items():
        if isinstance(value, np.ndarray):
            new_args.append(value)
        else:
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, list) is False:
                        good_type = False
                if good_type is True:
                    new_args.append(np.array(value))
            else:
                good_type = False
        if good_type is False:
            raise TypeError(
                'Type {} of variable \'{}\' is not supported. Use ndarray or '
                'list of lists instead.'.format(type(value).__name__, key))
        if np.issubdtype(new_args[-1].dtype, np.number) is False:
            raise TypeError(
                'Array \'{}\' should only contain numbers!'.format(key))

    if len(new_args) == 1:
        new_args = new_args[0]
    else:
        new_args = tuple(new_args)
    return new_args


def empty(**kwargs):
    """Checks if numpy arrays are empty.

    Parameters
    ----------
    kwargs : ndarray
        Arrays.

    Raises
    -------
    ValueError
        If any of the ndarrays are empty.
    """
    for key, value in kwargs.items():
        if value.size == 0:
            raise ValueError('Array \'{}\' is empty!'. format(key))


def match_shape(**kwargs):
    """Checks if numpy arrays have matching dimensions.

    Parameters
    ----------
    kwargs : tuple of ndarray and int
        Arrays and the dimension along which they should be matched.

    Raises
    -------
    ValueError
        If any of the ndarrays do not match specified dimensions.
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


def negative_array(**kwargs):
    """Checks if any entries in numpy arrays contain negative values.

    Parameters
    ----------
    kwargs : ndarray
        Arrays.

    Raises
    -------
    ValueError
        If any of the ndarrays contain negative values.
    """
    for key, value in kwargs.items():
        if (value < 0).any():
            raise ValueError(
                'Array \'{}\' contains at least one negative value!'.format(key)
            )


def negative_number(**kwargs):
    """Checks if any of the numbers are negative.

    Parameters
    ----------
    kwargs : int or float
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
            display.message(
                'Warning: some crossbar devices have zero resistance!',
                **kwargs)
