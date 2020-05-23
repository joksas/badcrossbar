"""
In perfect conditions, crossbar array can work as a dot product engine computing matrix products of applied voltages and the conductances of crossbar devices. However, when interconnect resistance is non-zero, crossbars deviate from this behaviour. This package computes branch currents and node voltages of the crossbar for arbitrary values of devices' resistances, applied voltages and interconnect resistance.

For most users, function badcrossbar.compute should complete the main task at hand, i.e. computing crossbar currents and voltages.
"""
from setuptools import setup

setup(
    name='badcrossbar',
    version='1.0.0',
    packages=['badcrossbar', 'badcrossbar.ideal', 'badcrossbar.nonideal', 'tests'],
    url='https://github.com/joksas/badcrossbar',
    license='MIT license',
    author='Dovydas Joksas',
    author_email='dovydas.joksas.15@ucl.ac.uk',
    description='Nodal analysis solver for memristive crossbar arrays.'
)
