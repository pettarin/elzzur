#!/usr/bin/env python
# coding=utf-8

"""
Set elzzur package up.
"""

from setuptools import setup, Extension

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

setup(
    name="elzzur",
    packages=["elzzur"],
    package_data={"elzzur": ["res/*"]},
    version="0.0.1.0",
    description="elzzur solves a Ruzzle board, listing all the valid words with their scores.",
    author="Alberto Pettarin",
    author_email="alberto@albertopettarin.it",
    url="https://github.com/pettarin/elzzur",
    license="MIT License",
    long_description=open("README.rst", "r").read(),
    install_requires=["marisa-trie>=0.7.2"],
    scripts=["bin/elzzur"],
    keywords=[
        "elzzur",
        "Ruzzle",
        "Ramble",
        "Scrabble",
        "Scarabeo",
        "Paroliere",
        "Snake",
        "board",
        "snake",
        "snakes",
        "solve",
        "solver",
        "MARISA",
        "trie",
        "prefix tree"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Desktop Environment",
        "Topic :: Utilities"
    ],
)
