"""
In perfect conditions, crossbar array can work as a dot product engine computing matrix products of applied voltages and the conductances of crossbar devices. However, when interconnect resistance is non-zero, crossbars deviate from this behaviour. This package computes output currents for arbitrary values of interconnect resistance.

For most users, function badcrossbar.currents should complete the main task at hand, i.e. computing output currents of a crossbar array given applied voltages, resistances of crossbar devices and interconnect resistance.
"""

from .compute import currents
