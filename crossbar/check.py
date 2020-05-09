import numpy as np

def crossbar_requirements(resistances, voltages):
    resistances, voltages = matrix_type(resistances, voltages)
    match_shape()
    non_zero()

    return resistances, voltages


def matrix_type(*args):
    new_args = []
    for i, arg in enumerate(args):
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
