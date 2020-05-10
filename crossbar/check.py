import numpy as np


def crossbar_requirements(resistances, voltages, r_i):
    """Checks if crossbar variables satisfy all requirements.

    :param resistances: Resistances of crossbar devices.
    :param voltages: Applied voltages.
    :param r_i: Interconnect resistance.
    :return: Potentially modified resistances and voltages.
    """
    resistances, voltages = matrix_type(resistances=resistances, voltages=voltages)
    empty(resistances=resistances, voltages=voltages)
    match_shape(resistances=(resistances, 0), voltages=(voltages, 0))
    number(r_i=r_i)
    short_circuit(resistances, r_i)

    return resistances, voltages


def number(**kwargs):
    """Confirms that items are int or float.

    :param kwargs: Items of arbitrary type.
    :return: None or raises an error if a certain item is neither int, nor float.
    """
    for key, value in kwargs.items():
        if not isinstance(value, int):
            if not isinstance(value, float):
                raise TypeError('Type ' + str(type(value)) + ' of variable \'' + key + '\' is not supported. Use int or float instead.')


def matrix_type(**kwargs):
    """Checks if items can be used numpy arrays.

    If one of the arguments is already a numpy array, it is returned unchanged. If it is a list (or a list of list), it is converted to numpy array and then returned. Else, an error is raised.

    :param kwargs: Items that should ideally already be numpy arrays.
    :return: Numpy arrays or raises an error.
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

    :param kwargs: Numpy arrays.
    :return: None or raises an error.
    """
    for key, value in kwargs.items():
        if value.size == 0:
            raise ValueError('Array \'' + key + '\' is empty!')


def match_shape(**kwargs):
    """Check if numpy arrays have matching dimensions; if not, raises an error.

    :param kwargs: Tuples of numpy arrays and dimensions that have to be matched.
    :return: None or raises an error.
    """
    first_key = list(kwargs.keys())[0]
    first_value = list(kwargs.values())[0]
    dim = first_value[0].shape[first_value[1]]
    for key, value in kwargs.items():
        if value[0].shape[value[1]] != dim:
            raise ValueError('Dimension ' + str(value[1]) + ' of array \'' + key + '\' should match dimension ' + str(first_value[1]) + ' of array \'' + first_key + '\'!')


def short_circuit(resistances, r_i):
    """Checks if crossbar will be short-circuited.

    :param resistances: Resistances of crossbar devices.
    :param r_i: Interconnect resistance.
    :return: None or raises an error.
    """
    if r_i == 0:
        if 0 in resistances:
            raise ValueError('At least some crossbar devices have zero resistance causing short circuit!')
