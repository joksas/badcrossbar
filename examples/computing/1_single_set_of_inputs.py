import badcrossbar

# Applied voltages in volts.
# 2D arrays must be used to avoid ambiguity.
applied_voltages = [
    [1.5],
    [2.3],
    [1.7],
]

# Device resistances in ohms.
resistances = [
    [345, 903, 755, 257, 646],
    [652, 401, 508, 166, 454],
    [442, 874, 190, 244, 635],
]

# Interconnect resistance in ohms.
r_i = 0.5

# Computing the solution.
solution = badcrossbar.compute(applied_voltages, resistances, r_i)

# Printing the current through the word line segment to the left of device in
# the second row and fourth column (Python uses zero-based indexing).
current = solution.currents.word_line[1, 3]
print(f"\nThe current through the word line segment is ~{current:.3g} A.")

# Printing the current at the third output (even when only one set of inputs
# is applied, it is necessary to specify the first index, in this case -- `0`).
current = solution.currents.output[0, 2]
print(f"\nThe current at the third output is ~{current:.3g} A.")

# Printing the current through the crossbar device in the last row and the
# last column (in Python, `-1` refers to the last element in an array).
current = solution.currents.device[-1, -1]
print(f"\nThe current through the crossbar device is ~{current:.3g} A.")

# Printing the voltage on the bit line node in the last row and second column.
voltage = solution.voltages.bit_line[-1, 1]
print(f"\nThe voltage at the bit line node is ~{voltage:.3g} V.")
