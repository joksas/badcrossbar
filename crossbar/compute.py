from crossbar import solve, extract, fill


def currents(voltages, resistances, r_i=0):
    r = fill.r(resistances, r_i)
    v = fill.v(voltages, resistances)
    i = solve.i(r, v)
    output_currents = extract.currents(i, resistances)

    return output_currents
