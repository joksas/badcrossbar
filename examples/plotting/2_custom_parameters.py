import numpy as np
import badcrossbar

# Plotting  submodule produces vector images (as a PDF file) that can then be
# edited in any vector graphics manipulation program. However, it also provides
# option to modify some of the features of the diagram that might be difficult
# to change once the image is produced.

# This example demonstrates how to use some of these options. In particular,
# we consider how one might visually represent node voltages in a large crossbar
# array where using default parameters produces a diagram with nodes that are
# hard to see without zooming in.

# shape of the crossbar array
num_word_lines = 128
num_bit_lines = 64

# number of different sets of inputs applied
num_examples = 100

# interconnect resistance in ohms
r_i = 0.25

# randomly generated resistances and voltages (in ohms and volts, respectively)
resistances = 100*np.random.rand(num_word_lines, num_bit_lines)
voltages = np.random.rand(num_word_lines, num_examples)

solution = badcrossbar.compute(voltages, resistances, r_i, verbose=0)

# we are going to make the interconnects and crossbar devices 4 times thinner
my_wire_scaling_factor = 1/4
my_device_scaling_factor = 1/4
# we are also going to make them lighter
my_default_color = (0.9, 0.9, 0.9)

# when we reduced the width of the devices, we also made the diameter of the
# nodes smaller (the two are controlled by the same variable
# `device_scaling_factor`. However, we want to make the nodes larger; for
# that we can use a separate variable `node_scaling_factor` which controls
# the size of the nodes without affecting the device width.
# the following line will result in net scaling factor of 10 for the nodes
my_node_scaling_factor = 1/my_device_scaling_factor * 10

# additionally, we are going to change the color bar colors, so that the
# zero would associated with black and that the maximum positive value would be
# associated with red
my_zero_rgb = (0, 0, 0)
my_high_rgb = (1, 0, 0)

badcrossbar.plot.voltages(all_voltages=solution.voltages,
                          wire_scaling_factor=my_wire_scaling_factor,
                          device_scaling_factor=my_device_scaling_factor,
                          default_color=my_default_color,
                          node_scaling_factor=my_node_scaling_factor,
                          zero_rgb=my_zero_rgb,
                          high_rgb=my_high_rgb,
                          filename='Ex-2',
                          allow_overwrite=True)

# The produced diagram hopefully helps to visualize the voltage decreases
# across the crossbar array more clearly. In this specific example, the
# new diagram has nodes that are larger than the crossbar devices (visible when
# zoomed in). However, this might be appropriate design decision if one
# wanted to have a better global view of how the voltages are distributed.
