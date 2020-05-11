import numpy as np


def crossbar_requirements(resistances, voltages, r_i):
    """Checks if crossbar variables satisfy all requirements.

    Parameters
    ----------
    resistances : array_like
        Resistances of crossbar devices.
    voltages : array_like
        Applied voltages.
    r_i : int, float
        Interconnect resistance.

    Returns
    -------
    resistances, voltages : ndarray
        Potentially modified resistances and voltages.
    """
    resistances, voltages = matrix_type(resistances=resistances, voltages=voltages)
    empty(resistances=resistances, voltages=voltages)
    match_shape(resistances=(resistances, 0), voltages=(voltages, 0))
    number(r_i=r_i)
    negative_array(resistances=resistances)
    negative_number(r_i=r_i)
    short_circuit(resistances, r_i)

    return resistances, voltages


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
        if not isinstance(value, int):
            if not isinstance(value, float):
                raise TypeError('Type ' + str(type(value)) + ' of variable \'' + key + '\' is not supported. Use int or float instead.')


def matrix_type(**kwargs):
    """Checks if items can be used numpy arrays.

    If one of the arguments is already a numpy array, it is returned unchanged. If it is a list (or a list of list), it is converted to numpy array and then returned. Else, an error is raised.

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
        If any of the items are not ndarray or list.
    """
    new_args = []
    for key, value in kwargs.items():
        if isinstance(value, np.ndarray):
            new_args.append(value)
        else:
            if isinstance(value, list):
                new_args.append(np.array(value))
            else:
                raise TypeError('Type ' + str(type(value)) + ' of variable \'' + key + '\' is not supported. Use np.ndarray or list instead.')

    if len(new_args) == 1:
        new_args = new_args[0]
    else:
        new_args = tuple(new_args)
    return new_args


def empty(**kwargs):
    """Checks if numpy arrays are empty; if yes, raises an error.

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
            raise ValueError('Array \'' + key + '\' is empty!')


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
            raise ValueError('Dimension ' + str(value[1]) + ' of array \'' + key + '\' should match dimension ' + str(first_value[1]) + ' of array \'' + first_key + '\'!')


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
            raise ValueError('Array \'' + str(key) + '\' contains at least one negative value!')


def negative_number(**kwargs):
    """Checks if any of the numbers are negative.

    Parameters
    ----------
    kwargs : int
        Numbers.

    Raises
    -------
    ValueError
        If any of the numbers are negative.
    """
    for key, value in kwargs.items():
        if value < 0:
            raise ValueError('Variable \'' + str(key) + '\' is negative!')


def short_circuit(resistances, r_i):
    """Checks if crossbar will be short-circuited.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i : int or float
        Interconnect resistance.

    Raises
    -------
    ValueError
        If r_i = 0 and any of the devices have zero resistance.
    """
    if r_i == 0:
        if 0 in resistances:
            raise ValueError('At least some crossbar devices have zero resistance causing short circuit!')
