import badcrossbar.computing as computing
import numpy as np
from scipy.sparse import lil_matrix
from collections import namedtuple
import copy
import pytest

Interconnect = namedtuple('Interconnect', ['word_line', 'bit_line'])
r_i = Interconnect(0.5, 0.25)

conductances_list = [
        np.array([[100], [0]]),
        np.array([[20, 50]]),
        np.array([[42]]),
        np.array([[0, 20], [30, 0]])]

g_matrices = [
        lil_matrix((4, 4)),
        lil_matrix((4, 4)),
        lil_matrix((2, 2)),
        lil_matrix((8, 8))]

# word_line_nodes
word_line_nodes_expected = [
        np.array([
            [102, 0, -100, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]),
        np.array([
            [24, -2, -20, 0],
            [-2, 52, 0, -50],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]),
        np.array([
            [44, -42],
            [0, 0]]),
        np.array([
            [4, -2, 0, 0, 0, 0, 0, 0],
            [-2, 22, 0, 0, 0, -20, 0, 0],
            [0, 0, 34, -2, 0, 0, -30, 0],
            [0, 0, -2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]])]

word_line_nodes_inputs = [i for i in zip(
    conductances_list, g_matrices, word_line_nodes_expected)]

# bit_line_nodes
bit_line_nodes_expected = [
        np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [-100, 0, 104, -4],
            [0, 0, -4, 8]]),
        np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [-20, 0, 24, 0],
            [0, -50, 0, 54]]),
        np.array([
            [0, 0],
            [-42, 46]]),
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, -4, 0],
            [0, -20, 0, 0, 0, 24, 0, -4],
            [0, 0, -30, 0, -4, 0, 38, 0],
            [0, 0, 0, 0, 0, -4, 0, 8]])]

bit_line_nodes_inputs = [i for i in zip(
    conductances_list, g_matrices, bit_line_nodes_expected)]

@pytest.mark.parametrize('conductances,g_matrix,expected', word_line_nodes_inputs)
def test_word_line_nodes(conductances, g_matrix, expected):
    """Tests `badcrossbar.computing.kcl.word_line_nodes()`.
    """
    filled_g_matrix = computing.kcl.word_line_nodes(
            copy.deepcopy(g_matrix), conductances, r_i).toarray()
    np.testing.assert_array_almost_equal(filled_g_matrix, expected)


@pytest.mark.parametrize('conductances,g_matrix,expected', bit_line_nodes_inputs)
def test_bit_line_nodes(conductances, g_matrix, expected):
    """Tests `badcrossbar.computing.kcl.bit_line_nodes()`.
    """
    filled_g_matrix = computing.kcl.bit_line_nodes(
            copy.deepcopy(g_matrix), conductances, r_i).toarray()
    np.testing.assert_array_almost_equal(filled_g_matrix, expected)

