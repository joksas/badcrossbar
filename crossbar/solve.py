from scipy.sparse import linalg


def i(r, v):
    i_matrix = linalg.spsolve(r.tocsc(), v)
    return i_matrix
