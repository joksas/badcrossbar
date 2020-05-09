import numpy as np


def crossbar_requirements(resistances, voltages, r_i):
    resistances, voltages = matrix_type(resistances=resistances, voltages=voltages)
    empty(resistances=resistances, voltages=voltages)
    match_shape(resistances=(resistances, 0), voltages=(voltages, 0))
    short_circuit(resistances, r_i)

    return resistances, voltages


def matrix_type(**kwargs):
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
    for key, value in kwargs.items():
        if value.size == 0:
            raise ValueError('Array \'' + key + '\' is empty!')


def match_shape(**kwargs):
    first_key = list(kwargs.keys())[0]
    first_value = list(kwargs.values())[0]
    dim = first_value[0].shape[first_value[1]]
    for key, value in kwargs.items():
        if value[0].shape[value[1]] != dim:
            raise ValueError('Dimension ' + str(value[1]) + ' of array \'' + key + '\' should match dimension ' + str(first_value[1]) + ' of array \'' + first_key + '\'!')


def short_circuit(resistances, r_i):
    if r_i == 0:
        if 0 in resistances:
            raise ValueError('At least some crossbar devices have zero resistance causing short circuit!')
