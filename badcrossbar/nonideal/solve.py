from scipy.sparse import linalg
from badcrossbar import display


def v(g, i):
    """Solves matrix equation gv = i.

    Parameters
    ----------
    g : ndarray
        Matrix containing conductances next to each of the nodes.
    i : ndarray
        Matrix containing known currents flowing into each of the nodes.

    Returns
    -------
    ndarray
        Matrix containing potentials at each of the nodes.
    """
    display.message('Started solving for v.')
    v_matrix = linalg.spsolve(g.tocsc(), i)
    display.message('Solved for v.')
    if v_matrix.ndim == 1:
        v_matrix = v_matrix.reshape(v_matrix.shape[0], 1)
    return v_matrix
