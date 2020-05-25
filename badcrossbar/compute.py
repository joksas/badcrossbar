from badcrossbar import check, nonideal, ideal, display


def compute(applied_voltages, resistances, r_i, **kwargs):
    """Computes branch currents and node voltages of a crossbar.

    Parameters
    ----------
    applied_voltages : array_like
        Applied voltages. Voltages must be supplied in an array of shape m x
        p, where m is the number of word lines and p is the number of
        examples (sets of voltages applied one by one).
    resistances : array_like
        Resistances of crossbar devices. Resistances must be supplied in an
        array of shape m x n, where n is the number of bit lines.
    r_i : int or float
        Interconnect resistance. It is assumed that all interconnects have
        the same resistance.
    kwargs
        node_voltages : bool, optional
            If False, None is returned instead of node voltages.
        all_currents : bool, optional
            If False, only output currents are returned, while all the other
            ones are set to None.
        verbose : int, optional
            If 0, no messages are shown. If 1, all messages are shown. If
            anything else, only warnings are shown.
    Returns
    -------
    named tuple
        Branch currents and node voltages of the crossbar. Field 'currents'
        is a named tuple itself with fields 'output', 'device', 'word_line'
        and 'bit_line' and contains output currents, as well as currents
        flowing through the devices and interconnect segments of the word and
        bit lines. Field 'voltages' is a named tuple itself with fields
        'word_line' and 'bit_line' and contains the voltages at the nodes on
        the word and bit lines. 'currents.output' is an array of shape p x n,
        while all the others are arrays of shape m x n if p = 1, or lists of
        length p with arrays of shape m x n as their elements if p > 1.
    """
    display.message('Initialising simulation.', **kwargs)
    resistances, applied_voltages = check.crossbar_requirements(
        resistances, applied_voltages, r_i, **kwargs)
    if r_i != 0:
        solution = nonideal.extract.solution(resistances, r_i, applied_voltages,
                                             **kwargs)
    else:
        solution = ideal.extract.solution(resistances, applied_voltages,
                                          **kwargs)

    return solution
