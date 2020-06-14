import badcrossbar
import numpy as np
import pickle
from collections import namedtuple
import pytest

Solution = namedtuple('Solution', ['currents', 'voltages'])
Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])

# the outputs of the function crossbar.compute are tested using the results
# from Qucs circuit simulation software.
single_input_names = ['1x1_a', '1x1_b', '1x1_c', '1x1_d', '1x1_e', '1x4_a',
                      '1x4_b', '1x4_c', '1x4_d', '1x4_e', '5x1_a', '5x1_b',
                      '5x1_c', '5x4_a', '5x4_b', '5x4_c', '5x4_d', '5x4_e',
                      '5x4_f', '5x4_g', '5x4_h']
multiple_input_names = [['5x4_a_v_1', '5x4_a_v_2', '5x4_a_v_3'],
                        ['5x4_b_v_1', '5x4_b_v_2', '5x4_b_v_3']]


@pytest.mark.parametrize('filename', single_input_names)
def test_currents_qucs(filename):
    resistances, voltages, r_i, expected_solution = qucs_data(filename)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i)
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize('filename', single_input_names)
def test_voltages_qucs(filename):
    resistances, voltages, r_i, expected_solution = qucs_data(filename)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i)
    compare_voltages(computed_solution.voltages, expected_solution.voltages)


@pytest.mark.parametrize('filenames', multiple_input_names)
def test_currents_qucs_multiple_inputs(filenames):
    resistances, voltages, r_i, expected_solution = qucs_data_multiple(
        filenames)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i)
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize('filenames', multiple_input_names)
def test_voltages_qucs_multiple_inputs(filenames):
    resistances, voltages, r_i, expected_solution = qucs_data_multiple(
        filenames)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i)
    compare_voltages(computed_solution.voltages, expected_solution.voltages)


def qucs_data(file_name):
    path = 'qucs/' + file_name + '.pickle'
    with open(path, 'rb') as handle:
        resistances, voltages, r_i, i_o, i_d, i_w, i_b, v_w, v_b = pickle.load(
            handle)

    extracted_currents = Currents(i_o, i_d, i_w, i_b)
    extracted_voltages = Voltages(v_w, v_b)

    solution = Solution(extracted_currents, extracted_voltages)

    return resistances, voltages, r_i, solution


def qucs_data_multiple(filenames):
    voltages_list = []
    i_o_list = []
    i_d_list = []
    i_w_list = []
    i_b_list = []
    v_w_list = []
    v_b_list = []

    for filename in filenames:
        path = 'qucs/' + filename + '.pickle'
        with open(path, 'rb') as handle:
            resistances, voltages, r_i, i_o, i_d, i_w, i_b, v_w, v_b = \
                pickle.load(handle)
        voltages_list.append(voltages)
        i_o_list.append(i_o)
        i_d_list.append(i_d[:, :, np.newaxis])
        i_w_list.append(i_w[:, :, np.newaxis])
        i_b_list.append(i_b[:, :, np.newaxis])
        v_w_list.append(v_w[:, :, np.newaxis])
        v_b_list.append(v_b[:, :, np.newaxis])

    voltages = np.concatenate(voltages_list, axis=1)
    i_o = np.concatenate(i_o_list, axis=0)
    i_d = np.concatenate(i_d_list, axis=2)
    i_w = np.concatenate(i_w_list, axis=2)
    i_b = np.concatenate(i_b_list, axis=2)
    v_w = np.concatenate(v_w_list, axis=2)
    v_b = np.concatenate(v_b_list, axis=2)

    extracted_currents = Currents(i_o, i_d, i_w, i_b)
    extracted_voltages = Voltages(v_w, v_b)

    solution = Solution(extracted_currents, extracted_voltages)

    return resistances, voltages, r_i, solution


def compare_currents(computed_currents, expected_currents):
    np.testing.assert_array_almost_equal(computed_currents.output,
                                         expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device,
                                         expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line,
                                         expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line,
                                         expected_currents.bit_line)


def compare_voltages(computed_voltages, expected_voltages):
    np.testing.assert_array_almost_equal(computed_voltages.word_line,
                                         expected_voltages.word_line)
    np.testing.assert_array_almost_equal(computed_voltages.bit_line,
                                         expected_voltages.bit_line)
