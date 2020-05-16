import numpy as np
from collections import namedtuple


def extract(filename, shape):
    data = open_file(filename)
    R = two_dim(data, shape, var1='R')
    V = one_dim(data, shape, var1='V')
    S = solution(data, shape)
    r_i = zero_dim(data, var1='r_i')
    pass


def open_file(filename):
    with open(filename, 'r') as opened_file:
        contents = opened_file.read()
    return contents


def two_dim(data, shape, var1, var2=None):
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
    delim1 = '<indep ' + var1
    if var2 is not None:
        delim1 += var2
    delim1 += ' 1>\n'
    delim2 = '\n</indep>'
    text = between(data, delim1, delim2)
    return float(text)


def solution(data, shape):
    Solution = namedtuple('Solution', ['currents', 'voltages'])

    device_currents = two_dim(data, shape, var1='d', var2='.I')
    word_line_currents = two_dim(data, shape, var1='w', var2='.I')
    bit_line_currents = two_dim(data, shape, var1='b', var2='.I')
    output_currents = bit_line_currents[-1, :]
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_currents, device_currents, word_line_currents, bit_line_currents)

    word_line_voltages = two_dim(data, shape, var1='w', var2='.V')
    bit_line_voltages = two_dim(data, shape, var1='b', var2='.V')
    Voltages = namedtuple('Currents', ['word_line', 'bit_line'])
    extracted_voltages = Voltages(word_line_voltages, bit_line_voltages)

    solution = Solution(extracted_currents, extracted_voltages)

    return solution


def between(data, delim1, delim2):
    return data.split(delim1)[1].split(delim2)[0]
