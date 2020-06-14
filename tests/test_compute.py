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
    """Tests currents computed by badcrossbar with the ones computed in Qucs
    circuit simulation software.

    Parameters
    ----------
    filename : str
        Name of the Qucs file used.
    """
    resistances, applied_voltages, r_i, expected_solution = qucs_data(filename)
    computed_solution = badcrossbar.compute(applied_voltages, resistances, r_i)
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize('filename', single_input_names)
def test_voltages_qucs(filename):
    """Tests voltages computed by badcrossbar with the ones computed in Qucs
    circuit simulation software.

    Parameters
    ----------
    filename : str
        Name of the Qucs file used.
    """
    resistances, applied_voltages, r_i, expected_solution = qucs_data(filename)
    computed_solution = badcrossbar.compute(applied_voltages, resistances, r_i)
    compare_voltages(computed_solution.voltages, expected_solution.voltages)


@pytest.mark.parametrize('filenames', multiple_input_names)
def test_currents_qucs_multiple_inputs(filenames):
    """Tests currents computed by badcrossbar with the ones computed in Qucs
    circuit simulation software when applying multiple inputs.

    Parameters
    ----------
    filenames : str
        Names of the Qucs files used.
    """
    resistances, applied_voltages, r_i, expected_solution = qucs_data_multiple(
        filenames)
    computed_solution = badcrossbar.compute(applied_voltages, resistances, r_i)
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize('filenames', multiple_input_names)
def test_voltages_qucs_multiple_inputs(filenames):
    """Tests voltages computed by badcrossbar with the ones computed in Qucs
    circuit simulation software when applying multiple inputs.

    Parameters
    ----------
    filenames : str
        Names of the Qucs files used.
    """
    resistances, applied_voltages, r_i, expected_solution = qucs_data_multiple(
        filenames)
    computed_solution = badcrossbar.compute(applied_voltages, resistances, r_i)
    compare_voltages(computed_solution.voltages, expected_solution.voltages)


def qucs_data(filename):
    """Extracts setup and solution of a particular Qucs file.
    
    Extraction is done by using pre-processed pickle file which was created 
    using qucs/extract.py.
        
    Parameters
    ----------
    filename : str
        Name of the Qucs file.

    Returns
    -------
    resistances : ndarray
        Resistances of crossbar devices.
    applied_voltages : ndarray
        Applied voltages.
    r_i : int or float
        Interconnect resistance.
    solution : named tuple
        Branch currents and node voltages of the crossbar.
    """
    path = 'qucs/' + filename + '.pickle'
    with open(path, 'rb') as handle:
        resistances, applied_voltages, r_i, i_o, i_d, i_w, i_b, v_w, v_b = \
            pickle.load(handle)

    extracted_currents = Currents(i_o, i_d, i_w, i_b)
    extracted_voltages = Voltages(v_w, v_b)

    solution = Solution(extracted_currents, extracted_voltages)

    return resistances, applied_voltages, r_i, solution


def qucs_data_multiple(filenames):
    """Extracts setups and solutions of particular Qucs files.

    Extraction is done by using pre-processed pickle files which were created
    using qucs/extract.py.

    Parameters
    ----------
    filenames : str
        Names of the Qucs file.

    Returns
    -------
    resistances : ndarray
        Resistances of crossbar devices.
    applied_voltages : ndarray
        Applied voltages (combined from multiple files).
    r_i : int or float
        Interconnect resistance.
    solution : named tuple
        Branch currents and node voltages of the crossbar (combined from
        multiple files).
    """
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
    """Compares currents.

    Parameters
    ----------
    computed_currents : named tuple of ndarray
        Computed crossbar branch currents.
    expected_currents : named tuple of ndarray
        Expected crossbar branch currents.
    """
    np.testing.assert_array_almost_equal(computed_currents.output,
                                         expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device,
                                         expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line,
                                         expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line,
                                         expected_currents.bit_line)


def compare_voltages(computed_voltages, expected_voltages):
    """Compares voltages.

    Parameters
    ----------
    computed_voltages : named tuple of ndarray
        Computed crossbar node voltages.
    expected_voltages : named tuple of ndarray
        Expected crossbar node voltages.
    """
    np.testing.assert_array_almost_equal(computed_voltages.word_line,
                                         expected_voltages.word_line)
    np.testing.assert_array_almost_equal(computed_voltages.bit_line,
                                         expected_voltages.bit_line)
