from scipy.sparse import linalg
import extract
import fill


def currents(voltages, resistances, r_i=0):
    r = fill.fill_r(resistances, r_i)
    v = fill.fill_v(voltages, resistances)
    i = solve(r, v)
    output_currents = extract.currents(i, resistances)

    return output_currents


def solve(r, v):
    i = linalg.spsolve(r.tocsc(), v)
    return i
