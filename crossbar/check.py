import numpy as np


def crossbar_requirements(resistances, voltages):
    resistances, voltages = matrix_type(resistances, voltages)
    empty(resistances, voltages)
    match_shape((resistances, 0), (voltages, 0))

    return resistances, voltages


def matrix_type(*args):
    new_args = []
    for arg in args:
        if isinstance(arg, np.ndarray):
            new_args.append(arg)
        else:
            if isinstance(arg, list):
                new_args.append(np.array(arg))
            else:
                raise TypeError('Type ' + str(type(arg)) + ' is not supported. Use np.ndarray or list instead.')

    if len(new_args) == 1:
        new_args = new_args[0]
    else:
        new_args = tuple(new_args)
    return new_args


def empty(*args):
    for arg in args:
        if arg.size == 0:
            raise ValueError('Array is empty!')


def match_shape(*args):
    dim = args[0][0].shape[args[0][1]]
    for arg in args:
        if arg[0].shape[arg[1]] != dim:
            raise ValueError('Array shapes do not match!')
