"""
In perfect conditions, crossbar array can work as a dot product engine
computing matrix products of applied voltages and the conductances of
crossbar devices. However, when interconnect resistance is non-zero,
crossbars deviate from this behaviour. This package computes branch currents
and node voltages of the crossbar for arbitrary values of devices'
resistances, applied voltages and interconnect resistance. Additionally,
it allows to plot currents and voltages (or other variables) in the crossbar
branches and nodes, respectively.

For most users, functions `badcrossbar.compute()`,
`badcrossbar.plot.branches()` and `badcrossbar.plot.nodes()` should complete
the main  task at hand, i.e. computing and plotting crossbar currents and
voltages.
"""
from setuptools import setup


def load_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


setup(
    name='badcrossbar',
    version='1.0.1',
    packages=['badcrossbar', 'badcrossbar.computing',
              'badcrossbar.plotting', 'tests'],
    install_requires=load_requirements(),
    url='https://github.com/joksas/badcrossbar',
    license='MIT license',
    author='Dovydas Joksas',
    author_email='dovydas.joksas.15@ucl.ac.uk',
    description='A Python tool for computing and plotting currents and '
                'voltages in passive crossbar arrays.'
)
