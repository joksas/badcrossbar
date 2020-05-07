import numpy as np


def currents(i, resistances, extract_all=False):
    output_i = np.transpose(i[-resistances.shape[1]:, ])
    if extract_all is False:
        return output_i
    else:
        device_i = device_currents(i, resistances)
        horizontal_i = horizontal_currents(i, resistances)
        vertical_i = vertical_currents(i, resistances)
        return output_i, device_i, horizontal_i, vertical_i


def device_currents(i, resistances):
    i_domain = i[:resistances.size, ]
    return reshaped_currents(i_domain, resistances)


def horizontal_currents(i, resistances):
    i_domain = i[resistances.size:2*resistances.size, ]
    return reshaped_currents(i_domain, resistances)


def vertical_currents(i, resistances):
    i_domain = i[2*resistances.size:3*resistances.size, ]
    return reshaped_currents(i_domain, resistances)


def reshaped_currents(i, resistances):
    if i.ndim > 1:
        reshaped_i = []
        for example in range(i.shape[1]):
            reshaped_i.append(i[:, example].reshape(resistances.shape))
    else:
        reshaped_i = i.reshape(resistances.shape)

    return reshaped_i


def reduced_resistances(resistances, voltages):
    # find rows that are not infinite
    rows = np.where(np.all(resistances == np.inf, axis=1) == False)[0]
    if len(rows) != 0:
        row = rows[0]
        resistances = resistances[row:, :]
        voltages = voltages[row:, :]

    # find columns that are infinite
    columns = np.where(np.all(resistances == np.inf, axis=0) == True)[0]
    if len(columns) != 0:
        column = columns[0]
        resistances = resistances[:, :column]

    return resistances, voltages
