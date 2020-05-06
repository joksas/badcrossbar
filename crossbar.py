from scipy.sparse import lil_matrix, csr_matrix

def currents(voltages, resistances, r_i=0):
    (num_inputs, num_outputs) = resistances.shape
    num_examples = voltages.shape[1]
    r = fill_r(resistances, r_i)
    v = fill_v(voltages)
    i = solve(r, v)
    currents = extract_currents(i)

    return currents


def fill_r(resistances, r_i):
    num_resistances = resistances.size
    r_shape = tuple(3*num_resistances for _ in range(2))
    r = lil_matrix(r_shape)
    r = kvl(r, resistances, r_i)
    r = kcl(r)
    return r
