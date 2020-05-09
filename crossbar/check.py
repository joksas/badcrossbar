def crossbar_requirements(resistances, voltages):
    resistances, voltages = matrix_type(resistances, voltages)
    match_shape()
    non_zero()

    return resistances, voltages
