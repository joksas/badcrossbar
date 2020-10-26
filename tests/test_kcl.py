import badcrossbar.computing as computing
import numpy as np
from scipy.sparse import lil_matrix
from collections import namedtuple
import pytest

Interconnect = namedtuple('Interconnect', ['word_line', 'bit_line'])
r_i = Interconnect(0.5, 0.25)
conductances = np.array([[100],
                         [0]])
g_matrix = lil_matrix((4, 4))

def test_word_line_nodes():
    """Tests `badcrossbar.computing.kcl.word_line_nodes()`.
    """
    filled_g_matrix = computing.kcl.word_line_nodes(
            g_matrix, conductances, r_i).toarray()
    expected = np.array([[102, 0, -100, 0],
                         [0, 2, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    np.testing.assert_array_almost_equal(filled_g_matrix, expected)

