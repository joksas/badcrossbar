from collections import namedtuple
from pathlib import Path

import badcrossbar
import numpy as np
import pytest
from badcrossbar import utils

Solution = namedtuple("Solution", ["currents", "voltages"])
Currents = namedtuple("Currents", ["output", "device", "word_line", "bit_line"])
Voltages = namedtuple("Voltages", ["word_line", "bit_line"])

# the outputs of the function crossbar.compute are tested using the results
# from Qucs circuit simulation software.
single_input_1x1 = [
    "1x1-{}-{}".format(letter, number)
    for letter in ["a", "b", "c", "d", "e"]
    for number in [1, 2, 3]
]
single_input_5x4 = [
    "5x4-{}-{}".format(letter, number)
    for letter in ["a", "b", "c", "d", "e", "f"]
    for number in [1, 2, 3]
]
single_input_names = single_input_1x1 + single_input_5x4

multiple_inputs_1x1 = [
    ["1x1-{}-{}".format(letter, number) for number in [1, 2, 3]]
    for letter in ["a", "b", "c", "d", "e"]
]
multiple_inputs_5x4 = [
    ["5x4-{}-{}".format(letter, number) for number in [1, 2, 3]]
    for letter in ["a", "b", "c", "d", "e", "f"]
]
multiple_input_names = multiple_inputs_1x1 + multiple_inputs_5x4


@pytest.mark.parametrize("filename", single_input_names)
def test_currents_qucs(filename):
    """Tests currents computed by badcrossbar with the ones computed in Qucs
    circuit simulation software.

    Parameters
    ----------
    filename : str
        Name of the Qucs file used.
    """
    resistances, applied_voltages, r_i_word_line, r_i_bit_line, expected_solution = qucs_data(
        filename
    )
    computed_solution = badcrossbar.compute(
        applied_voltages, resistances, None, r_i_word_line, r_i_bit_line
    )
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize("filename", single_input_names)
def test_voltages_qucs(filename):
    """Tests voltages computed by badcrossbar with the ones computed in Qucs
    circuit simulation software.

    Parameters
    ----------
    filename : str
        Name of the Qucs file used.
    """
    resistances, applied_voltages, r_i_word_line, r_i_bit_line, expected_solution = qucs_data(
        filename
    )
    computed_solution = badcrossbar.compute(
        applied_voltages, resistances, None, r_i_word_line, r_i_bit_line
    )
    compare_voltages(computed_solution.voltages, expected_solution.voltages)


@pytest.mark.parametrize("filenames", multiple_input_names)
def test_currents_qucs_multiple_inputs(filenames):
    """Tests currents computed by badcrossbar with the ones computed in Qucs
    circuit simulation software when applying multiple inputs.

    Parameters
    ----------
    filenames : str
        Names of the Qucs files used.
    """
    (
        resistances,
        applied_voltages,
        r_i_word_line,
        r_i_bit_line,
        expected_solution,
    ) = qucs_data_multiple(filenames)
    computed_solution = badcrossbar.compute(
        applied_voltages, resistances, None, r_i_word_line, r_i_bit_line
    )
    compare_currents(computed_solution.currents, expected_solution.currents)


@pytest.mark.parametrize("filenames", multiple_input_names)
def test_voltages_qucs_multiple_inputs(filenames):
    """Tests voltages computed by badcrossbar with the ones computed in Qucs
    circuit simulation software when applying multiple inputs.

    Parameters
    ----------
    filenames : str
        Names of the Qucs files used.
    """
    (
        resistances,
        applied_voltages,
        r_i_word_line,
        r_i_bit_line,
        expected_solution,
    ) = qucs_data_multiple(filenames)
    computed_solution = badcrossbar.compute(
        applied_voltages, resistances, None, r_i_word_line, r_i_bit_line
    )
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
    r_i_word_line : int or float
        Interconnect resistance of the word line segments.
    r_i_bit_line : int or float
        Interconnect resistance of the bit line segments.
    solution : named tuple
        Branch currents and node voltages of the crossbar.
    """
    path = Path(__file__).parent / Path("qucs/{}.pickle".format(filename))
    (
        resistances,
        applied_voltages,
        r_i_word_line,
        r_i_bit_line,
        i_o,
        i_d,
        i_w,
        i_b,
        v_w,
        v_b,
    ) = utils.load_pickle(path)

    extracted_currents = Currents(i_o, i_d, i_w, i_b)
    extracted_voltages = Voltages(v_w, v_b)

    solution = Solution(extracted_currents, extracted_voltages)

    return resistances, applied_voltages, r_i_word_line, r_i_bit_line, solution


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
    r_i_word_line : int or float
        Interconnect resistance of the word line segments.
    r_i_bit_line : int or float
        Interconnect resistance of the bit line segments.
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
        path = Path(__file__).parent / Path("qucs/{}.pickle".format(filename))
        (
            resistances,
            applied_voltages,
            r_i_word_line,
            r_i_bit_line,
            i_o,
            i_d,
            i_w,
            i_b,
            v_w,
            v_b,
        ) = utils.load_pickle(path)

        voltages_list.append(applied_voltages)
        i_o_list.append(i_o)
        i_d_list.append(i_d[:, :, np.newaxis])
        i_w_list.append(i_w[:, :, np.newaxis])
        i_b_list.append(i_b[:, :, np.newaxis])
        v_w_list.append(v_w[:, :, np.newaxis])
        v_b_list.append(v_b[:, :, np.newaxis])

    applied_voltages = np.concatenate(voltages_list, axis=1)
    i_o = np.concatenate(i_o_list, axis=0)
    i_d = np.concatenate(i_d_list, axis=2)
    i_w = np.concatenate(i_w_list, axis=2)
    i_b = np.concatenate(i_b_list, axis=2)
    v_w = np.concatenate(v_w_list, axis=2)
    v_b = np.concatenate(v_b_list, axis=2)

    extracted_currents = Currents(i_o, i_d, i_w, i_b)
    extracted_voltages = Voltages(v_w, v_b)

    solution = Solution(extracted_currents, extracted_voltages)

    return resistances, applied_voltages, r_i_word_line, r_i_bit_line, solution


def compare_currents(computed_currents, expected_currents):
    """Compares currents.

    Parameters
    ----------
    computed_currents : named tuple of ndarray
        Computed crossbar branch currents.
    expected_currents : named tuple of ndarray
        Expected crossbar branch currents.
    """
    np.testing.assert_array_almost_equal(computed_currents.output, expected_currents.output)
    np.testing.assert_array_almost_equal(computed_currents.device, expected_currents.device)
    np.testing.assert_array_almost_equal(computed_currents.word_line, expected_currents.word_line)
    np.testing.assert_array_almost_equal(computed_currents.bit_line, expected_currents.bit_line)


def compare_voltages(computed_voltages, expected_voltages):
    """Compares voltages.

    Parameters
    ----------
    computed_voltages : named tuple of ndarray
        Computed crossbar node voltages.
    expected_voltages : named tuple of ndarray
        Expected crossbar node voltages.
    """
    np.testing.assert_array_almost_equal(computed_voltages.word_line, expected_voltages.word_line)
    np.testing.assert_array_almost_equal(computed_voltages.bit_line, expected_voltages.bit_line)
