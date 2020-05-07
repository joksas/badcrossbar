import numpy as np


def currents(i, resistances, extract_all=True):
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
