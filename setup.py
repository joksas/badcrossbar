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
import os
import pathlib

import setuptools

DIR_PATH = pathlib.Path(__file__).parent
REQUIREMENTS_PATH = DIR_PATH / "requirements.txt"
README_PATH = DIR_PATH / "README.md"

setuptools.setup(
    name="badcrossbar",
    version="1.1.0",
    packages=["badcrossbar", "badcrossbar.computing", "badcrossbar.plotting", "tests"],
    install_requires=REQUIREMENTS_PATH.read_text().splitlines(),
    url="https://github.com/joksas/badcrossbar",
    project_urls={
        "Bug Tracker": "https://github.com/joksas/badcrossbar/issues",
        "Documentation": "https://badcrossbar.readthedocs.io",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Dovydas Joksas",
    author_email="dovydas.joksas.15@ucl.ac.uk",
    description="A Python tool for computing and plotting currents and "
    "voltages in passive crossbar arrays.",
    long_description=README_PATH.read_text(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
)
