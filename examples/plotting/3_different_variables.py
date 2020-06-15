import badcrossbar

# The main purpose of plotting module is for plotting currents and voltages
# in the branches and on the nodes of the crossbar, respectively. However,
# these functions can accept any numeric arrays and thus plot arbitrary
# variables. This example shows how to plot the percentage change in current
# in every branch, due to introduced line resistance.

# applied voltages in volts
applied_voltages = [[1.5],
                    [2.3],
                    [1.7]]

# device resistances in ohms
resistances = [[345, 903, 755, 257, 646],
               [652, 401, 508, 166, 454],
               [442, 874, 190, 244, 635]]

# interconnect resistance in ohms
r_i_ideal = 0
r_i_nonideal = 0.5

# computing the solution
solution_ideal = badcrossbar.compute(
    applied_voltages, resistances, r_i_ideal, verbose=0)
solution_nonideal = badcrossbar.compute(
    applied_voltages, resistances, r_i_nonideal, verbose=0)

# extracting the currents
ideal_currents = solution_ideal.currents
nonideal_currents = solution_nonideal.currents

# computing percentage changes
device_change = (nonideal_currents.device -
                 ideal_currents.device)/ideal_currents.device * 100
word_line_change = (nonideal_currents.word_line -
                    ideal_currents.word_line)/ideal_currents.word_line * 100
bit_line_change = (nonideal_currents.bit_line -
                   ideal_currents.bit_line)/ideal_currents.bit_line * 100

# plotting percentage changes
modified_label = 'Change in current (%)'
badcrossbar.plot.currents(device_currents=device_change,
                          word_line_currents=word_line_change,
                          bit_line_currents=bit_line_change,
                          axis_label=modified_label,
                          filename='Ex-3',
                          allow_overwrite=True)
