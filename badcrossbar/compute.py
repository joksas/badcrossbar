from badcrossbar import check, nonideal, ideal


def compute(voltages, resistances, r_i=0, **kwargs):
    """Computes currents and voltages in a crossbar.

    Parameters
    ----------
    voltages : array_like
        Applied voltages. Voltages must be supplied in an array of shape m x p, where m is the number of word lines and p is the number of examples (sets of voltages applied one by one).
    resistances : array_like
        Resistances of crossbar devices. Resistances must be supplied in an array of shape m x n, where n is the number of bit lines.
    r_i : int or float
        Interconnect resistance. It is assumed that all interconnects have the same resistance.
    kwargs
        node_voltages : bool, optional
            If False, None is returned instead of node voltages.
        all_currents : bool, optional
            If False, only output currents are returned, while all the other ones are set to None.
    Returns
    -------
    named tuple
        Currents and voltages of the crossbar. Field 'currents' is a named tuple itself with fields 'output', 'device', 'word_line' and 'bit_line' and contains output currents, as well as currents flowing through the devices and interconnect segments of the word and bit lines. Field 'voltages' is a named tuple itself with fields 'word_line' and 'bit_line' and contains the potentials at the nodes on the word and bit lines. 'currents.output' is an array of shape p x n, while all the others are arrays of shape m x n if p = 1, or lists of length p with arrays of shape m x n as their elements if p > 1.
    """
    resistances, voltages = check.crossbar_requirements(resistances, voltages, r_i)
    if r_i != 0:
        solution = nonideal.extract.solution(resistances, r_i, voltages, **kwargs)
    else:
        solution = ideal.extract.solution(resistances, voltages, **kwargs)

    return solution
