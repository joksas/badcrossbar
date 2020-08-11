import badcrossbar

# The main purpose of the plotting module is for plotting currents and voltages
# in the branches and on the nodes of the crossbar, respectively. However,
# these functions can accept any numeric arrays and thus plot arbitrary
# variables. This example shows how to plot the percentage change in current
# in every branch, due to introduced line resistance.

# Applied voltages in volts.
applied_voltages = [[1.5],
                    [2.3],
                    [1.7]]

# Device resistances in ohms.
resistances = [[345, 903, 755, 257, 646],
               [652, 401, 508, 166, 454],
               [442, 874, 190, 244, 635]]

# Interconnect resistance in ohms (different for word and bit line segments).
r_i_ideal = {'word_line': 0, 'bit_line': 0}
r_i_nonideal = {'word_line': 0.75, 'bit_line': 0.5}

# Computing the solution.
solution_ideal = badcrossbar.compute(
    applied_voltages, resistances, verbose=0,
    r_i_word_line=r_i_ideal['word_line'], r_i_bit_line=r_i_ideal['bit_line'])
solution_nonideal = badcrossbar.compute(
    applied_voltages, resistances, verbose=0,
    r_i_word_line=r_i_nonideal['word_line'],
    r_i_bit_line=r_i_nonideal['bit_line'])

# Extracting the currents.
ideal_currents = solution_ideal.currents
nonideal_currents = solution_nonideal.currents

# Computing percentage changes.
device_change = (nonideal_currents.device -
                 ideal_currents.device)/ideal_currents.device * 100
word_line_change = (nonideal_currents.word_line -
                    ideal_currents.word_line)/ideal_currents.word_line * 100
bit_line_change = (nonideal_currents.bit_line -
                   ideal_currents.bit_line)/ideal_currents.bit_line * 100

# Plotting percentage changes.
modified_label = 'Change in current (%)'
badcrossbar.plot.branches(device_vals=device_change,
                          word_line_vals=word_line_change,
                          bit_line_vals=bit_line_change,
                          axis_label=modified_label,
                          filename='Ex-3',
                          allow_overwrite=True)
