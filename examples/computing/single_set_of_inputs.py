import badcrossbar

# applied voltages in volts
# 2D arrays must be used to avoid ambiguity
applied_voltages = [[1.5],
                    [2.3],
                    [1.7]]

# device resistances in ohms
resistances = [[345, 903, 755, 257, 646],
               [652, 401, 508, 166, 454],
               [442, 874, 190, 244, 635]]

# interconnect resistance in ohms
r_i = 0.5

# computing the solution
solution = badcrossbar.compute(applied_voltages, resistances, r_i)

# printing the current through the word line segment to the left of device in
# the second row and fourth column
current = solution.currents.word_line[1, 3]
print('\nThe current through the word line segment is {} A.'.format(current))
