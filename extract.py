def extract_currents(i, resistances):
    output_currents = i[-resistances.shape[1]:, ]

    return output_currents
