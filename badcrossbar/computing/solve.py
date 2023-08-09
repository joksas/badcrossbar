import logging

import jax
import jax.numpy as jnp
import numpy as np
import numpy.typing as npt
from badcrossbar.computing import fill
from jax.scipy.sparse import linalg
from jax.experimental.sparse import BCOO

logger = logging.getLogger(__name__)


def v(resistances: npt.NDArray, r_i, applied_voltages: npt.NDArray):
    """Solves matrix equation `gv = i`.

    Args:
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.
        applied_voltages: Applied voltages.

    Returns:
        Matrix containing potentials at each of the nodes.
    """
    if r_i.word_line > 0 or r_i.bit_line > 0:
        g = fill.g(resistances, r_i)
        g_indices = []
        g_data = []
        for (row, col) in g:
            g_indices.append([row, col])
            g_data.append(g[(row, col)])

        i = fill.i(applied_voltages, resistances, r_i)
        g_matrix = BCOO((g_data, g_indices), shape=(i.shape[0], i.shape[0]))

        solver = jax.jit(linalg.cg)
        logger.info("Started solving for v.")
        v_matrix, _ = solver(g_matrix, i, tol=1e-12, atol=1e-12)
        logger.info("Solved for v.")

        v_matrix = np.array(v_matrix)
        # if `num_examples == 1`, it can result in 1D array.
        if v_matrix.ndim == 1:
            v_matrix = v_matrix.reshape(v_matrix.shape[0], 1)

        # if one of the interconnect resistances is zero, only half of the
        # matrix_v had to be solved. The other half can be filled without
        # solving because the node voltages are known.
        if r_i.word_line == 0:
            new_v_matrix = np.zeros((2 * resistances.size, applied_voltages.shape[1]))
            new_v_matrix[
                : resistances.size,
            ] = np.repeat(applied_voltages, resistances.shape[1], axis=0)
            new_v_matrix[
                resistances.size :,
            ] = v_matrix
            v_matrix = new_v_matrix
        if r_i.bit_line == 0:
            new_v_matrix = np.zeros((2 * resistances.size, applied_voltages.shape[1]))
            new_v_matrix[
                : resistances.size,
            ] = v_matrix
            v_matrix = new_v_matrix
    else:
        # if both interconnect resistances are zero, all node voltages are
        # known.
        v_matrix = np.zeros((2 * resistances.size, applied_voltages.shape[1]))
        v_matrix[
            : resistances.size,
        ] = np.repeat(applied_voltages, resistances.shape[1], axis=0)

    return v_matrix
