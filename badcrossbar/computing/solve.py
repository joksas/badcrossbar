from scipy.sparse import linalg
from badcrossbar import utils


def v(g, i, **kwargs):
    """Solves matrix equation gv = i.

    Parameters
    ----------
    g : lil_matrix
        Matrix containing conductances next to each of the nodes.
    i : ndarray
        Matrix containing known currents flowing into each of the nodes.

    Returns
    -------
    ndarray
        Matrix containing potentials at each of the nodes.
    """
    utils.message('Started solving for v.', **kwargs)
    v_matrix = linalg.spsolve(g.tocsc(), i)
    utils.message('Solved for v.', **kwargs)
    if v_matrix.ndim == 1:
        v_matrix = v_matrix.reshape(v_matrix.shape[0], 1)
    return v_matrix
