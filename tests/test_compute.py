import badcrossbar
import numpy as np
import pickle
from collections import namedtuple
import pytest

# the outputs of the function crossbar.compute are tested using the results
# from Qucs circuit simulation software.
file_names = ['1x1_a', '1x1_b', '1x1_c', '1x1_d', '1x1_e', '1x4_a', '1x4_b',
              '1x4_c', '1x4_d', '1x4_e', '5x1_a', '5x1_b', '5x1_c', '5x4_a',
              '5x4_b', '5x4_c', '5x4_d', '5x4_e', '5x4_f', '5x4_g', '5x4_h']
double_inputs = [False, True]


@pytest.mark.parametrize('file_name', file_names)
@pytest.mark.parametrize('double_input', double_inputs)
def test_currents_qucs(file_name, double_input):
    resistances, voltages, r_i, expected_solution = qucs_data(
        file_name, double_input=double_input)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i)
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize('file_name', file_names)
@pytest.mark.parametrize('double_input', double_inputs)
def test_voltages_qucs(file_name, double_input):
    resistances, voltages, r_i, expected_solution = qucs_data(
        file_name, double_input=double_input)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i)
    compare_voltages(computed_solution.voltages, expected_solution.voltages)


def qucs_data(file_name, double_input=False):
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    Currents = namedtuple('Currents',
                          ['output', 'device', 'word_line', 'bit_line'])
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])

    path = 'qucs/' + file_name + '.pickle'
    with open(path, 'rb') as handle:
        resistances, voltages, r_i, i_o, i_d, i_w, i_b, v_w, v_b = pickle.load(
            handle)

    if double_input:
        i_o = np.repeat(i_o, 2, axis=0)
        i_d = np.repeat(i_d[:, :, np.newaxis], 2, axis=2)
        i_w = np.repeat(i_w[:, :, np.newaxis], 2, axis=2)
        i_b = np.repeat(i_b[:, :, np.newaxis], 2, axis=2)
        v_w = np.repeat(v_w[:, :, np.newaxis], 2, axis=2)
        v_b = np.repeat(v_b[:, :, np.newaxis], 2, axis=2)
        voltages = np.repeat(voltages, 2, axis=1)

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
