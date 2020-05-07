import extract
import fill
import solve


def currents(voltages, resistances, r_i=0):
    r = fill.r(resistances, r_i)
    v = fill.v(voltages, resistances)
    i = solve.solve(r, v)
    output_currents = extract.currents(i, resistances)

    return output_currents
