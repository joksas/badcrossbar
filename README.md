## About

[badcrossbar] is a nodal analysis solver for crossbar arrays that suffer from line resistance. It solves for currents in all the branches, as well as for voltages at all the nodes of the crossbar.

## Background

Conventional crossbars have a structure like the one shown in the image below. Resistive two-terminal **devices** (depicted here as memristors) are connected to **word lines** on one side and to **bit lines** on the other. In the diagram, the crossbar devices are depicted in black, the word lines are depicted as horizontal blue lines and the bit lines as vertical blue lines. Orange circles denote the **nodes**, i.e. the connections between the devices and the word/bit lines. The segments of word and bit lines between neighbouring nodes are often seen as **interconnects** between neighbouring devices and can themselves be modelled as resistive elements.

![crossbar array](images/3x5-crossbar-array.png)

In most practical scenarios, we want the resistance of the interconnects to be zero. That is because crossbar arrays containing resistive elements can be used as dot product engines, i.e. systems able to compute vector-matrix products in hardware. Specifically, crossbar arrays with interconnect resistance of zero are able to compute the vector-matrix products of applied voltages (vector) and conductances of the crossbar devices (matrix). In the diagram above, voltages are applied on the left side of the word lines and the vector-matrix product is computed in a form of currents at the bottom of the bit lines.

## Usage

[badcrossbar] computes branch currents and node voltages for arbitrary values of applied voltages, devices' resistances and interconnect resistance. It assumes that all interconnects have the same specified resistance.

One can compute branch currents and node voltages with the code shown in the example below.

```python
import badcrossbar

# applied voltages in volts
applied_voltages = [[1.5],
                    [2.3],
                    [1.7]]

# device resistances in ohms
resistances = [[345, 903, 755, 257, 646],
               [652, 401, 508, 166, 454],
               [442, 874, 190, 244, 635]]

# interconnect resistance in ohms
r_i = 0.5

solution = badcrossbar.compute(applied_voltages, resistances, r_i)
```

The returned variable (`solution`) is a named tuple with fields `currents` and `voltages`.

### Currents

`solution.currents` is itself a named tuple with fields `output`, `device`, `word_line` and `bit_line`. The first field represents the output currents, while the rest represent the currents flowing through devices, interconnects along the word lines, and interconnects along the bit lines. All of these branches are depicted in the diagram below.

![crossbar array](images/3x5-crossbar-array-branches.png)

If `applied_voltages` is an array of shape `(m, p)` (each column representing a different set of inputs) and `resistances` is an array of shape `(m, n)`, then:
* `currents.output` will be a [numpy] array of shape `(p, n)`.
* `currents.device`,  `currents.word_line` and `currents.bit_line` will be [numpy] arrays of shape `(m, n)` if `p = 1`, or will be lists of length `p` containing [numpy] arrays of shape `(m, n)` as their elements if `p > 1`.

### Voltages

`solution.voltages` is itself a named tuple with fields `word_line` and `bit_line`. They represent the voltages at the nodes on the word and bit lines, respectively. These two types of nodes are depicted in the diagram below.

![crossbar array](images/3x5-crossbar-array-nodes.png)

If `applied_voltages` is an array of shape `(m, p)` (each column representing a different set of inputs) and `resistances` is an array of shape `(m, n)`, then `voltages.word_line` and `voltages.bit_line` will be [numpy] arrays of shape `(m, n)` if `p = 1`, or will be lists of length `p` containing [numpy] arrays of shape `(m, n)` as their elements if `p > 1`.

### Example

Suppose we applied four sets of inputs to a crossbar array and wanted to find the current flowing through the device in the first row and fourth column when the second set of inputs was applied. We could print out the current through that device using the following piece of code:

```python
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

solution = badcrossbar.compute(applied_voltages, resistances, r_i)

# current that we are interested in (note zero-based indexing)
current = solution.currents.device[1][0, 3]

print('\nCurrent through the device in question is {} A.'.format(current))
```

#### Output

```text
2020-05-23 10:54:28     Started solving for v.
2020-05-23 10:54:28     Solved for v.
2020-05-23 10:54:28     Extracted node voltages.
2020-05-23 10:54:28     Extracted currents from all branches in the crossbar.

Current through the device in question is 0.015489677765099288 A.
```

### Perfectly insulating devices

Devices with infinite resistance can be denoted using resistance value of `numpy.inf` (or equivalently `math.inf`).

[badcrossbar]:https://github.com/joksas/badcrossbar
[numpy]:https://github.com/numpy/numpy