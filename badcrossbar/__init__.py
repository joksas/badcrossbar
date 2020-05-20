"""
In perfect conditions, crossbar array can work as a dot product engine computing matrix products of applied voltages and the conductances of crossbar devices. However, when interconnect resistance is non-zero, crossbars deviate from this behaviour. This package computes output currents for arbitrary values of crossbar devices' resistances, applied voltages and interconnect resistance.

For most users, function badcrossbar.compute should complete the main task at hand, i.e. computing crossbar currents and voltages.
"""

from .compute import compute
