#!/usr/bin/env python
# coding=utf-8

"""
A Snake represents a (possibly partial) list of adjacent board cells,
represented by ``(x, y)`` pairs, 0-indexing.
"""

from __future__ import absolute_import
from __future__ import print_function

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

class Snake(object):
    """
    A Snake represents a (possibly partial) list of adjacent board cells,
    represented by ``(x, y)`` pairs, 0-indexing.
    
    :param list cells: list of (x, y) pairs representing the cells of the snake
    """
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        return u" ".join(["(%d,%d)" % cell for cell in self.cells])

    def __len__(self):
        return len(self.cells)

    @property
    def start(self):
        """
        The cell where the snake starts.

        :rtype: (int, int)
        """
        return self.cells[0]

    @property
    def end(self):
        """
        The cell where the snake ends.

        :rtype: (int, int)
        """
        return self.cells[-1]
    
    def has_cell(self, cell):
        """
        Return ``True`` if the given ``(x, y)`` cell is already in the snake.

        :param tuple cell: the ``(x, y)`` cell to be checked for
        :rtype: bool
        """
        return cell in self.cells
    
    def extend(self, cell):
        """
        Return a new Snake which is the current Snake extended with the given cell.

        :param tuple cell: the ``(x, y)`` cell to be added
        :rtype: Snake
        """
        return Snake(self.cells + [cell])



