from collections import defaultdict

import jax.numpy as jnp
from jax import Array
from badcrossbar.computing import kcl


def g(resistances: Array, r_i) -> dict[(int, int), float]:
    """Creates and fills matrix `g` used in equation `gv = i`.

    Args:
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Filled matrix `g`.
    """
    g_matrix = defaultdict(float)
    g_matrix = kcl.apply(g_matrix, resistances, r_i)
    return g_matrix


def i(applied_voltages: Array, resistances: Array, r_i) -> Array:
    """Creates and fills matrix `i` used in equation `gv = i`.

    Values are filled by applying nodal analysis at the leftmost nodes on the
    word lines.

    Args:
        applied_voltages: Applied voltages.
        resistances: Resistances of crossbar devices.
        r_i: Interconnect resistances along the word and bit line segments.

    Returns:
        Filled matrix `i`.
    """
    if 0 in r_i:
        i_shape = (resistances.size, applied_voltages.shape[1])
    else:
        i_shape = (2 * resistances.size, applied_voltages.shape[1])
    i_matrix = jnp.zeros(i_shape)
    if r_i.word_line > 0:
        i_matrix = i_matrix.at[: resistances.size : resistances.shape[1], :].set(applied_voltages / r_i.word_line)
    else:
        i_matrix = jnp.divide(
            jnp.repeat(applied_voltages, resistances.shape[1], axis=0),
            jnp.repeat(resistances.reshape(resistances.size, 1), applied_voltages.shape[1], axis=1),
        )
    return i_matrix
