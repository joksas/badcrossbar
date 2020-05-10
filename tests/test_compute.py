import crossbar
import numpy as np
from collections import namedtuple


def test_currents_qucs_2x3_a():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[10, 20, 30],
                            [40, 50, 60]])
    voltages = np.array([[3],
                         [5]])
    r_i = 0.1

    expected_currents = Currents(np.array([[0.4109446865, 0.2427676365, 0.1782942773]]),
                                 np.array([[0.2877316742, 0.1442221472, 0.09620240051],
                                           [0.1232130123, 0.09854548924, 0.08209187684]]),
                                 np.array([[0.5281562219, 0.2404245477, 0.09620240051],
                                           [0.3038503784, 0.1806373661, 0.08209187684]]),
                                 np.array([[0.2877316742, 0.1442221472, 0.09620240051],
                                           [0.4109446865, 0.2427676365, 0.1782942773]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def test_currents_qucs_2x3_b():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[10, 20, 30],
                            [40, 50, 60]])
    voltages = np.array([[3],
                         [5]])
    r_i = 0

    expected_currents = Currents(np.array([[0.425, 0.25, 0.183333333333333]]),
                                 np.array([[0.3, 0.15, 0.1],
                                           [0.125, 0.1, 0.0833333333333]]),
                                 np.array([[0.55, 0.25, 0.1],
                                           [0.3083333333333, 0.183333333333, 0.08333333333333]]),
                                 np.array([[0.3, 0.15, 0.1],
                                           [0.425, 0.25, 0.183333333333333]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def test_currents_qucs_2x3_c():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[45, np.inf, np.inf],
                            [150, np.inf, 20]])
    voltages = np.array([[14],
                         [6]])
    r_i = 1.5

    expected_currents = Currents(np.array([[0.3160015477, 0, 0.228795581]]),
                                 np.array([[0.2817916183, 0, 0],
                                           [0.03420992942, 0, 0.228795581]]),
                                 np.array([[0.2817916183, 0, 0],
                                           [0.2630055104, 0.228795581, 0.228795581]]),
                                 np.array([[0.2817916183, 0, 0],
                                           [0.3160015477, 0, 0.228795581]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def compare_currents(computed_currents, expected_currents):
    np.testing.assert_array_almost_equal(computed_currents.output, expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device, expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line, expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line, expected_currents.bit_line)
