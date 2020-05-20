from collections import namedtuple
import numpy as np
from badcrossbar import display


def solution(resistances, applied_voltages, **kwargs):
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    extracted_voltages = voltages(applied_voltages, resistances)
    extracted_currents = currents(resistances, applied_voltages, extracted_voltages, **kwargs)
    if kwargs.get('node_voltages', True) is False:
        extracted_voltages = None
    else:
        display.message('Extracted node voltages.')
    extracted_solution = Solution(extracted_currents, extracted_voltages)
    return extracted_solution


def voltages(applied_voltages, resistances):
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])
    word_line_v = word_line_voltages(applied_voltages, resistances)
    bit_line_v = bit_line_voltages(applied_voltages, resistances)
    extracted_voltages = Voltages(word_line_v, bit_line_v)
    return extracted_voltages


def word_line_voltages(applied_voltages, resistances):
    if applied_voltages.shape[1] > 1:
        word_line_v = []
        for i in range(applied_voltages.shape[1]):
            word_line_v.append(np.repeat(applied_voltages[:, i:i+1], resistances.shape[1], axis=1))
    else:
        word_line_v = np.repeat(applied_voltages[:, 0:1], resistances.shape[1], axis=1)

    return word_line_v


def bit_line_voltages(applied_voltages, resistances):
    if applied_voltages.shape[1] > 1:
        bit_line_v = [np.zeros(resistances.shape) for _ in range(applied_voltages.shape[1])]
    else:
        bit_line_v = np.zeros(resistances.shape)

    return bit_line_v


def currents(resistances, applied_voltages, extracted_voltages, **kwargs):
    output_i = output_currents(resistances, applied_voltages)
    device_i = None
    word_line_i = None
    bit_line_i = None

    if kwargs.get('all_currents', True) is False:
        display.message('Extracted output currents.')
    else:
        device_i = device_currents(extracted_voltages.word_line, resistances)
        word_line_i = word_line_currents(resistances, device_i)
        bit_line_i = bit_line_currents(resistances, device_i)
        display.message('Extracted currents from all branches in the crossbar.')

    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    extracted_currents = Currents(output_i, device_i, word_line_i, bit_line_i)
    return extracted_currents


def output_currents(resistances, applied_voltages):
    output_i = np.dot(np.transpose(1./resistances), applied_voltages)

    return np.transpose(output_i)


def device_currents(extracted_voltages, resistances):
    if isinstance(extracted_voltages, list):
        device_i = []
        for voltages in extracted_voltages:
            device_i.append(np.divide(voltages, resistances))
    else:
        device_i = np.divide(extracted_voltages, resistances)

    return device_i


def word_line_currents(resistances, device_i_all):
    if isinstance(device_i_all, list):
        word_line_i = []
        for device_i in device_i_all:
            temp_word_line_i = np.zeros(resistances.shape)
            temp_word_line_i[:, :] += np.repeat(device_i[:, -1:], resistances.shape[1], axis=1)
            for i in range(1, resistances.shape[1]):
                temp_word_line_i[:, :-i] += np.repeat(device_i[:, -(1+i):-i], resistances.shape[1]-i, axis=1)
            word_line_i.append(temp_word_line_i)
    else:
        word_line_i = np.zeros(resistances.shape)
        word_line_i[:, :] += np.repeat(device_i_all[:, -1:], resistances.shape[1], axis=1)
        for i in range(1, resistances.shape[1]):
            word_line_i[:, :-i] += np.repeat(device_i_all[:, -(1 + i):-i], resistances.shape[1] - i, axis=1)

    return word_line_i


def bit_line_currents(resistances, device_i_all):
    if isinstance(device_i_all, list):
        bit_line_i = []
        for device_i in device_i_all:
            temp_bit_line_i = np.zeros(resistances.shape)
            for i in range(resistances.shape[0]):
                temp_bit_line_i[i:, :] += np.repeat(device_i[i:i+1, :], resistances.shape[0]-i, axis=0)
            bit_line_i.append(temp_bit_line_i)
    else:
        bit_line_i = np.zeros(resistances.shape)
        for i in range(resistances.shape[0]):
            bit_line_i[i:, :] += np.repeat(device_i_all[i:i + 1, :], resistances.shape[0] - i, axis=0)

    return bit_line_i
