from badcrossbar import check, nonideal, ideal


def compute(voltages, resistances, r_i=0, **kwargs):
    """Computes output currents for a crossbar.

    :param voltages: Applied voltages. Voltages must be supplied in an array of shape m x p, where m is the number of word lines and p is the number of examples (sets of voltages applied one by one).
    :param resistances: Resistances of crossbar devices. Resistances must be supplied in an array of shape m x n, where n is the number of bit lines.
    :param r_i: Interconnect resistance. It is assumed that all interconnects have the same resistance.
    :return: Currents in a crossbar. Output currents are returned in an array of shape p x n. If extract_all=False is not passed, then also currents flowing through crossbar devices, word lines and bit lines are returned as lists of arrays of shape m x n.
    """
    resistances, voltages = check.crossbar_requirements(resistances, voltages, r_i)
    if r_i != 0:
        solution = nonideal.extract.solution(resistances, r_i, voltages, **kwargs)
    else:
        solution = ideal.extract.solution(resistances, voltages, **kwargs)

    return solution
