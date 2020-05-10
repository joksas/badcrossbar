import crossbar
import numpy as np
from collections import namedtuple


def test_currents_qucs_2x3_a():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None.
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

    :return: None.
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

    This specific test returns an error if devices with infinite resistance are not converted to devices with very large resistance.

    :return: None.
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


def test_currents_qucs_2x3_d():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None.
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[np.inf, np.inf, np.inf],
                            [30, 45.5, np.inf]])
    voltages = np.array([[10],
                         [7]])
    r_i = 0.5

    expected_currents = Currents(np.array([[0.2234425948, 0.1465591213, 0]]),
                                 np.array([[0, 0, 0],
                                           [0.2234425948, 0.1465591213, 0]]),
                                 np.array([[0, 0, 0],
                                           [0.3700017161, 0.1465591213, 0]]),
                                 np.array([[0, 0, 0],
                                           [0.2234425948, 0.1465591213, 0]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def test_currents_qucs_2x1_a():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None.
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[60],
                            [10]])
    voltages = np.array([[3],
                         [0.1]])
    r_i = 1

    expected_currents = Currents(np.array([[0.0519205298]]),
                                 np.array([[0.04754966887],
                                           [0.004370860927]]),
                                 np.array([[0.04754966887],
                                           [0.004370860927]]),
                                 np.array([[0.04754966887],
                                           [0.0519205298]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def test_currents_qucs_2x1_b():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None.
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[100],
                            [500]])
    voltages = np.array([[0],
                         [0]])
    r_i = 1

    expected_currents = Currents(np.array([[0]]),
                                 np.array([[0],
                                           [0]]),
                                 np.array([[0],
                                           [0]]),
                                 np.array([[0],
                                           [0]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def test_currents_qucs_2x1_c():
    """Tests outputs of crossbar.compute.test_currents against results from Qucs.

    :return: None.
    """
    Currents = namedtuple('Currents', ['output', 'device', 'word_line', 'bit_line'])
    resistances = np.array([[1],
                            [np.inf]])
    voltages = np.array([[50],
                         [5]])
    r_i = 0

    expected_currents = Currents(np.array([[50]]),
                                 np.array([[50],
                                           [0]]),
                                 np.array([[50],
                                           [0]]),
                                 np.array([[50],
                                           [50]]))
    computed_currents = crossbar.currents(voltages, resistances, r_i=r_i)

    compare_currents(computed_currents, expected_currents)


def test_currents_dot_product_engine():
    """Tests whether crossbars behave as dot product engines when r_i = 0.

    When r_i = 0, crossbars should be able to compute matrix-vector products of conductances of devices and applied voltages.

    :return: None.
    """
    for _ in range(10):
        m, n, p = np.random.randint(1, 30, 3)
        resistances = np.random.rand(m, n)
        voltages = np.random.rand(m, p)
        r_i = 0
        computed_currents = crossbar.currents(voltages, resistances, r_i)

        conductances = np.reciprocal(resistances)
        expected_output = np.dot(np.transpose(voltages), conductances)

        np.testing.assert_array_almost_equal(computed_currents.output, expected_output)


def test_currents_dot_product_engine_insulating():
    """Tests whether crossbars behave as dot product engines when r_i = 0, but some devices are insulating.

    When r_i = 0, crossbars should be able to compute matrix-vector products of conductances of devices and applied voltages.

    :return: None.
    """
    for _ in range(10):
        m, n, p = np.random.randint(1, 30, 3)
        resistances = np.random.rand(m, n)
        rows = np.random.randint(0, m, int(0.1 * m * n))
        columns = np.random.randint(0, n, int(0.1 * m * n))
        resistances[rows, columns] = np.inf  # makes ~10% of random devices (some might be repeated) insulating

        voltages = np.random.rand(m, p)
        r_i = 0
        computed_currents = crossbar.currents(voltages, resistances, r_i)

        conductances = np.reciprocal(resistances)
        expected_output = np.dot(np.transpose(voltages), conductances)

        np.testing.assert_array_almost_equal(computed_currents.output, expected_output)


def test_currents_dot_product_engine_insulating_lines():
    """Tests whether crossbars behave as dot product engines when r_i = 0, but some word lines and bit lines contain only insulating devices.

    When r_i = 0, crossbars should be able to compute matrix-vector products of conductances of devices and applied voltages.

    :return: None.
    """
    for _ in range(10):
        m, n, p = np.random.randint(10, 30, 3)
        resistances = np.random.rand(m, n)
        rows = np.random.randint(0, m, int(0.3*m))
        columns = np.random.randint(0, n, int(0.3*n))
        resistances[rows, :] = np.inf  # makes ~30% of random word lines (some might be repeated) contain only insulating devices
        resistances[:, columns] = np.inf  # makes ~30% of random bit lines (some might be repeated) contain only insulating devices

        voltages = np.random.rand(m, p)
        r_i = 0
        computed_currents = crossbar.currents(voltages, resistances, r_i)

        conductances = np.reciprocal(resistances)
        expected_output = np.dot(np.transpose(voltages), conductances)

        np.testing.assert_array_almost_equal(computed_currents.output, expected_output)


def test_currents_return_only_outputs():
    """Tests whether the function returns only output currents and whether all the other parameters are None.

    :return: None.
    """
    m, n, p = np.random.randint(10, 30, 3)
    resistances = np.random.rand(m, n)
    voltages = np.random.rand(m, p)
    r_i = 0
    computed_currents = crossbar.currents(voltages, resistances, r_i, extract_all=False)

    assert type(computed_currents.output) is np.ndarray
    assert computed_currents.device is None
    assert computed_currents.word_line is None
    assert computed_currents.bit_line is None


def compare_currents(computed_currents, expected_currents):
    np.testing.assert_array_almost_equal(computed_currents.output, expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device, expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line, expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line, expected_currents.bit_line)
