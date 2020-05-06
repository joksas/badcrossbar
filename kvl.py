def apply(r, resistances, r_i):
    r = fill_resistances(r, resistances)
    r = fill_horizontal(r, r_i)
    r = fill_vertical(r, r_i)
    return r
