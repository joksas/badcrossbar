import badcrossbar

# Applied voltages in volts.
applied_voltages = [
    [1.5, 4.1, 2.6, 2.1],
    [2.3, 4.5, 1.1, 0.8],
    [1.7, 4.0, 3.3, 1.1],
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

# The function `badcrossbar.plot.branches` accepts either individual arrays for
# crossbar devices, word line branches and bit line branches, or a named tuple
# containing all currents. If any of the arrays are 3D, they are averaged along
# the third axis. Function `badcrossbar.plot.nodes` uses the same exact
# principle for plotting voltages at the nodes on the word and bit lines.

# Plotting average branch currents over all four sets of inputs.
# We additionally set a custom filename and label of the color bar,
# and allow to overwrite produced PDF files.
badcrossbar.plot.branches(
    currents=solution.currents,
    filename="Ex-1-1",
    axis_label="Average current (A)",
    allow_overwrite=True,
)

# Plotting average branch currents over all four sets of inputs, but only in
# the crossbar devices and the bit line segments (word line segments will
# be colored in black).
badcrossbar.plot.branches(
    device_vals=solution.currents.device,
    bit_line_vals=solution.currents.bit_line,
    filename="Ex-1-2",
    axis_label="Average current (A)",
    allow_overwrite=True,
)

# Plotting average node voltages over all four sets of inputs.
badcrossbar.plot.nodes(
    voltages=solution.voltages,
    filename="Ex-1-3",
    axis_label="Average voltage (V)",
    allow_overwrite=True,
)

# Plotting only the word line node voltages (bit line nodes will be colored
# in black) when the third set of inputs is applied.
badcrossbar.plot.nodes(
    word_line_vals=solution.voltages.word_line[:, :, 2], filename="Ex-1-4", allow_overwrite=True
)
