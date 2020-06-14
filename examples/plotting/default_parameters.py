import badcrossbar

# applied voltages in volts
applied_voltages = [[1.5, 4.1, 2.6, 2.1],
                    [2.3, 4.5, 1.1, 0.8],
                    [1.7, 4.0, 3.3, 1.1]]

# device resistances in ohms
resistances = [[345, 903, 755, 257, 646],
               [652, 401, 508, 166, 454],
               [442, 874, 190, 244, 635]]

# interconnect resistance in ohms
r_i = 0.5

# computing the solution
solution = badcrossbar.compute(applied_voltages, resistances, r_i)

"""
The function badcrossbar.plot.currents accepts either individual arrays for 
word line branches, bit line branches and crossbar devices or a named tuple 
containing all currents. If any of the arrays are 3D, they are averaged along 
the third axis. Function badcrossbar.plot.voltages uses the same exact 
principle for plotting voltages at the nodes on the word and bit lines.
"""

# plotting average branch currents over all four sets of inputs
badcrossbar.plot.currents(all_currents=solution.currents)

#  plotting average branch currents over all four sets of inputs, but only in
#  the crossbar devices and the bit line segments (word line segments will
#  be colored in black)
badcrossbar.plot.currents(device_currents=solution.currents.device,
                          bit_line_currents=solution.currents.bit_line)

# plotting average node voltages over all four sets of inputs
badcrossbar.plot.voltages(all_voltages=solution.voltages)

# plotting only the word line node voltages (bit line nodes will be colored
# in black) when the third set of inputs is applied
badcrossbar.plot.voltages(
    word_line_voltages=solution.voltages.word_line[:, :, 2])
