import badcrossbar

# Applied voltages in volts.
applied_voltages = [[1.5, 4.1, 2.6, 2.1],
                    [2.3, 4.5, 1.1, 0.8],
                    [1.7, 4.0, 3.3, 1.1]]

# Device resistances in ohms.
resistances = [[345, 903, 755, 257, 646],
               [652, 401, 508, 166, 454],
               [442, 874, 190, 244, 635]]

# Interconnect resistance in ohms.
r_i = 0.5

# Computing the solution.
solution = badcrossbar.compute(applied_voltages, resistances, r_i)

# Printing the current through the word line segment to the left of device in
# the second row and fourth column when the first set of inputs is applied
# (Python uses zero-based indexing).
current = solution.branches.word_line[1, 3, 0]
print('\nThe current through the word line segment is {} A.'.format(current))

# Printing the current at the third output when the second set of inputs is
# applied.
current = solution.branches.output[1, 2]
print('\nThe current at the third output is {} A.'.format(current))

# Printing the current through the crossbar device in the last row and the
# last column when the last set of inputs is applied (in Python, `-1` refers
# to the last element in an array).
current = solution.branches.device[-1, -1, -1]
print('\nThe current through the crossbar device is {} A.'.format(current))

# Printing the voltage on the bit line node in the last row and second column
# when the third set of inputs is applied.
voltage = solution.nodes.bit_line[-1, 1, 2]
print('\nThe voltage at the bit line node is {} V.'.format(voltage))
