from scipy.sparse import linalg
from crossbar import display


def i(r, v):
    display.message('Started solving for i.')
    i_matrix = linalg.spsolve(r.tocsc(), v)
    display.message('Solved for i.')
    return i_matrix
