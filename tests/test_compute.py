import badcrossbar
import numpy as np
import pickle
from collections import namedtuple
import pytest


@pytest.mark.parametrize('file_name', ['1x4_a', '1x4_b', '1x4_c', '1x4_d', '5x1_a', '5x1_b' '5x1_c', '5x4_a', '5x4_b', '5x4_c', '5x4_d', '5x4_e', '5x4_f', '5x4_g'])
def test_currents_qucs(file_name):
    resistances, voltages, r_i, expected_solution = qucs_data(file_name)
    computed_solution = badcrossbar.compute(voltages, resistances, r_i=r_i)
    compare_currents(computed_solution.currents, expected_solution.currents)


def qucs_data(file_name):
    Solution = namedtuple('Solution', ['currents', 'voltages'])
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    Voltages = namedtuple('Voltages', ['word_line', 'bit_line'])

    path = 'qucs-files/' + file_name + '.pickle'
    with open(path, 'rb') as handle:
        resistances, voltages, r_i, i_o, i_d, i_w, i_b, v_w, v_b = pickle.load(handle)

    extracted_currents = Currents(i_o, i_d, i_w, i_b)
    extracted_voltages = Voltages(v_w, v_b)
    solution = Solution(extracted_currents, extracted_voltages)

    return resistances, voltages, r_i, solution


def compare_currents(computed_currents, expected_currents):
    np.testing.assert_array_almost_equal(computed_currents.output, expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device, expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line, expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line, expected_currents.bit_line)
