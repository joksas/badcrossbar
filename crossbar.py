def currents(voltages, resistances, r_i=0):
    (num_inputs, num_outputs) = resistances.shape
    num_examples = voltages.shape[1]
    r = fill_r(resistances, r_i)
    v = fill_b(voltages)
    i = solve(r, v)
    currents = extract_currents(i)

    return currents
