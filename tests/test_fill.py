import badcrossbar.computing as computing
import numpy as np
from scipy.sparse import lil_matrix
from collections import namedtuple
import copy
import pytest

Interconnect = namedtuple('Interconnect', ['word_line', 'bit_line'])

applied_voltages_list = [
        np.array([
            [5]]),
        np.array([
            [5, 10, -4]]),
        np.array([
            [5],
            [7]]),
        np.array([
            [7, 11, 13],
            [-2, 0, 5]])]

resistances_list = [
        np.ones((1,1)),
        np.ones((1,1)),
        np.array([[10, 20], [30, 40]]),
        np.ones((2,2))]

r_i_list = [
        Interconnect(0.5, 0),
        Interconnect(0.5, 0.25),
        Interconnect(0, 0.25),
        Interconnect(0.5, 0.25)]

# i
i_expected = [
        np.array([
            [10]]),
        np.array([
            [10, 20, -8],
            [0, 0, 0]]),
        np.array([
            [5/10],
            [5/20],
            [7/30],
            [7/40]]),
        np.array([
            [14, 22, 26],
            [0, 0, 0],
            [-4, 0, 10],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])]

i_inputs = [i for i in zip(
    applied_voltages_list, resistances_list, r_i_list, i_expected)]


@pytest.mark.parametrize('applied_voltages,resistances,r_i,expected', i_inputs)
def test_i(applied_voltages, resistances, r_i, expected):
    """Tests `badcrossbar.computing.fill.i()`.
    """
    i_matrix = computing.fill.i(applied_voltages, resistances, r_i)
    np.testing.assert_array_almost_equal(i_matrix, expected)

