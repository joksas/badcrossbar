def currents(voltages, resistances, r=0):
    (num_inputs, num_outputs) = resistances.shape
    num_examples = voltages.shape[1]
    R = fill_R(resistances)
    V = fill_V(voltages)
    I = solve(R, V)
    currents = extract_currents(I)

    return currents
