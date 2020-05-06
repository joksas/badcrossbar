def apply(r, resistances):
    r = fill_left(r, resistances)
    r = fill_right(r, resistances)
    return r
