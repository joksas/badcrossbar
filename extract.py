def currents(i, resistances, extract_all=False):
    output_i = i[-resistances.shape[1]:, ]
    if extract_all is False:
        return output_i
    else:
        device_i = device_currents(i, resistances)
        horizontal_i = horizontal_currents(i, resistances)
        vertical_i = horizontal_currents(i, resistances)
        return output_i, device_i, horizontal_i, vertical_i


def device_currents(i, resistances):
    i = i[:resistances.size, ]
    if i.ndim > 1:
        device_i = []
        for example in range(i.shape[1]):
            device_i.append(i[:, example].reshape(resistances.shape))
    else:
        device_i = i.reshape(resistances.shape)

    return device_i
