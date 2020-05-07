from crossbar import solve, extract, fill
import numpy as np


def currents(voltages, resistances, r_i=0):
    """Computes output currents for a crossbar.

    :param voltages: Applied voltages. Voltages must be supplied in an array of shape m x p, where m is the number of word lines and p is the number of examples (sets of voltages applied one by one).
    :param resistances: Resistances of crossbar devices. Resistances must be supplied in an array of shape m x n, where n is the number of bit lines.
    :param r_i: Interconnect resistance. It is assumed that all interconnects have the same resistance.
    :return: Output currents. Currents are returned in an array of shape p x n.
    """
    complete_output_currents = np.zeros((voltages.shape[1], resistances.shape[1]))
    resistances, voltages = extract.reduced_resistances(resistances, voltages)
    r = fill.r(resistances, r_i)
    v = fill.v(voltages, resistances)
    i = solve.i(r, v)
    output_currents, device_currents, horizontal_currents, vertical_currents = extract.currents(i, resistances)
    complete_output_currents[:, :output_currents.shape[1]] = output_currents

    return output_currents, device_currents, horizontal_currents, vertical_currents
