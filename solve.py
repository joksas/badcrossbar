from scipy.sparse import linalg


def i(r, v):
    i = linalg.spsolve(r.tocsc(), v)
    return i
