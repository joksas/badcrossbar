from scipy.sparse import linalg


def solve(r, v):
    i = linalg.spsolve(r.tocsc(), v)
    return i