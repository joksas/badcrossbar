from crossbar import solve, extract, fill
import numpy as np


def currents(voltages, resistances, r_i=0):
    complete_output_currents = np.zeros((voltages.shape[1], resistances.shape[1]))
    resistances, voltages = extract.reduced_resistances(resistances, voltages)
    r = fill.r(resistances, r_i)
    v = fill.v(voltages, resistances)
    i = solve.i(r, v)
    output_currents = extract.currents(i, resistances)
    complete_output_currents[:, :output_currents.shape[1]] = output_currents

    return complete_output_currents
