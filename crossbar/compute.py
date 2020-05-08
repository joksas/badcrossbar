from crossbar import solve, extract, fill


def currents(voltages, resistances, r_i=0, **kwargs):
    """Computes output currents for a crossbar.

    :param voltages: Applied voltages. Voltages must be supplied in an array of shape m x p, where m is the number of word lines and p is the number of examples (sets of voltages applied one by one).
    :param resistances: Resistances of crossbar devices. Resistances must be supplied in an array of shape m x n, where n is the number of bit lines.
    :param r_i: Interconnect resistance. It is assumed that all interconnects have the same resistance.
    :return: Output currents. Currents are returned in an array of shape p x n.
    """
    # TODO: check that shapes are correct
    original_shape = extract.shapes(voltages, resistances)
    resistances, voltages = extract.reduced_resistances(resistances, voltages)
    r = fill.r(resistances, r_i)
    v = fill.v(voltages, resistances)
    i = solve.i(r, v)
    crossbar_currents = extract.currents(i, resistances, shape=original_shape, **kwargs)

    return crossbar_currents
