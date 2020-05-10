import crossbar
import numpy as np
from collections import namedtuple


def test_currents_qucs_2x3_a():
    """Tests outputs of crossbar.compute.test_currents against results Qucs.

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

    np.testing.assert_array_almost_equal(computed_currents.output, expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device, expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line, expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line, expected_currents.bit_line)

