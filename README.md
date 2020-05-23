##About

[badcrossbar] is a nodal analysis solver for crossbar arrays that suffer from line resistance. It solves for currents in all the branches, as well as for voltages at all the nodes of the crossbar.

##Background

Conventional crossbars have a structure like the one shown in the image below. Resistive two-terminal **devices** (depicted here as memristors) are connected to **word lines** on one side and to **bit lines** on the other. In the diagram, the crossbar devices are depicted in black, the word lines are the horizontal blue lines and the bit lines are the vertical blue lines. Orange circles denote the **nodes**, i.e. the connections between the devices and the word/bit lines. The segments of word and bit lines between neighbouring nodes are often seen as **interconnects** between neighbouring devices and can themselves be modelled as resistive elements.

![crossbar array](images/3x5_crossbar_array.png)

In most practical scenarios, we want the resistance of the interconnects to be zero. That is because crossbar arrays containing resistive elements can be used as dot product engines, i.e. systems able to compute vector-matrix products in hardware. Specifically, crossbar arrays with interconnect resistance of zero are able to compute the vector-matrix products of applied voltages (vector) and conductances of the crossbar devices (matrix). In the diagram above, voltages are applied on the left side of the word lines and the vector-matrix product is computed in a form of currents at the bottom of the bit lines.

##Usage

[badcrossbar] computed branch currents and node voltages for arbitrary values of applied voltages, devices' resistances and interconnect resistance. It assumes that all interconnects have the same specified resistance.

One can compute branch currents and node voltages with the code shown in the example below.

```python
import badcrossbar

# applied voltages in volts
applied_voltages = [[1.5],
                    [2.3],
                    [1.7]]

# device resistance in ohms
resistances = [[34, 90, 75, 25, 64],
               [65, 40, 50, 16, 45],
               [44, 87, 19, 24, 63]]

# interconnect resistance in ohms
r_i = 0.5

solution = badcrossbar.compute(applied_voltages, resistances, r_i)
```

The returned variable (`solution`) is a named tuple with fields `currents` and `voltages`.

###Currents

`solution.currents` is itself a named tuple with fields `output`, `device`, `word_line` and `bit_line`. The first field represents the output currents, while the rest represent the currents flowing through devices, interconnects along the word lines, and interconnects along the bit lines. All of these branches are depicted in the diagram below.

![crossbar array](images/3x5_crossbar_array_branches.png)

If `applied_voltages` is an array of shape `(m, p)` (each column representing a different set of inputs) and `resistances` is an array of shape `(m, n)`, then:
* `currents.output` will be a [numpy] array of shape `(p, n)`
* `currents.device`,  `currents.word_line` and `currents.bit_line` will be [numpy] arrays of shape `(m, n)` if `p = 1` or will be lists of length `p` containing [numpy] arrays of shape `(m, n)` as their elements.

###Voltages

`solution.voltages` is itself a named tuple with fields `word_line` and `bit_line`. They represent the voltages at the nodes on the word lines and bit lines, respectively. These two types of nodes are depicted in the diagram below.

![crossbar array](images/3x5_crossbar_array_nodes.png)

If `applied_voltages` is an array of shape `(m, p)` (each column representing a different set of inputs) and `resistances` is an array of shape `(m, n)`, then `voltages.word_line` and `voltages.bit_line` will be [numpy] arrays of shape `(m, n)` if `p = 1` or will be lists of length `p` containing [numpy] arrays of shape `(m, n)` as their elements.

[badcrossbar]:https://github.com/joksas/badcrossbar
[numpy]:https://github.com/numpy/numpy