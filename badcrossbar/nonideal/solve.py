from scipy.sparse import linalg
from badcrossbar import display
from badcrossbar.nonideal import extract


def i(r, v):
    """Solves matrix equation ri = v.

    :param r: r matrix.
    :param v: v matrix.
    :return: Currents in each branch of the crossbar.
    """
    display.message('Started solving for i.')
    r = extract.non_infinite(r)
    i_matrix = linalg.spsolve(r.tocsc(), v)  # converts lil_matrix to csc_matrix before solving
    display.message('Solved for i.')
    return i_matrix


def v(g, i):
    """Solves matrix equation ri = v.

    :param r: r matrix.
    :param v: v matrix.
    :return: Currents in each branch of the crossbar.
    """
    display.message('Started solving for i.')
    v_matrix = linalg.spsolve(g.tocsc(), i)  # converts lil_matrix to csc_matrix before solving
    display.message('Solved for v.')
    if v_matrix.ndim == 1:
        v_matrix = v_matrix.reshape(v_matrix.shape[0], 1)
    return v_matrix
