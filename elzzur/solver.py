#!/usr/bin/env python
# coding=utf-8

"""
Solve a Ruzzle board.

The idea is to do a BFS exploration of the board,
avoiding extending the current snake (i.e., adjacent sequence of letters),
if either
a. the snake self-intersects or,
b. the word corresponding to the current snake is not a prefix of any word in the dictionary.

To speed the lookup operations, the dictionary is stored in a MARISA trie,
which is a very efficient trie (a.k.a. prefix tree),
supporting the has_keys_with_prefix(prefix) operation.
"""

from __future__ import absolute_import
from __future__ import print_function

from elzzur.board import Board
from elzzur.mtdictionary import MTDictionary
from elzzur.snake import Snake

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

class Solver(object):
    """
    Solve a Ruzzle board.

    Please see the README.md for a discussion.

    :param Board board: the board to solve
    :param MTDictionary dictionary: the dictionary containing the valid words
    """

    SORT_BY_SCORE = "score"
    """ Sort by score (decr), length (inc), word (alpha) """

    SORT_BY_LENGTH = "length"
    """ Sort by length (decr), score (decr), word (alpha) """

    SORT_BY_START = "start"
    """ Sort by snake start position (NW->SE), score (decr), word (alpha) """

    SORT_BY_END = "end"
    """ Sort by snake end position (NW->SE), score (decr), word (alpha) """

    def __init__(self, board, dictionary):
        self.board = board
        self.dictionary = dictionary
        self.found = {}

    def solve(self, sort=SORT_BY_SCORE, reverse=False):
        """
        Solve the board.

        :param str sort: the sort method
        :param bool reverse: if ``True`` reverse the order of the words
        """
        self.found = {}
        # find all valid snakes
        for snake in self.find_snakes():
            # for each word, keep only the snake with the highest score
            snake_word = self.board.compute_snake_word(snake)
            snake_score = self.board.compute_snake_score(snake)
            if (snake_word not in self.found) or (self.found[snake_word][1] < snake_score):
                self.found[snake_word] = (snake_word, snake_score, snake)
        # sort and return
        return self.sort_words(sort=sort, reverse=reverse)

    def find_snakes(self):
        """
        Find all the valid snakes in the board.

        :rtype: list of Snake objects
        """
        valid_snakes = []
        rows = self.board.rows
        cols = self.board.cols
        for row in range(rows):
            for col in range(cols):
                to_be_explored = [Snake([(row, col)])]
                while len(to_be_explored) > 0:
                    current = to_be_explored.pop(0)
                    current_word = self.board.compute_snake_word(current)
                    if (len(current_word) > 1) and (self.dictionary.has_key(current_word)):
                        valid_snakes.append(current)
                    if self.dictionary.has_keys_with_prefix(current_word):
                        crow, ccol = current.end
                        for trow in range(max(0, crow - 1), min(rows, crow + 2)):       # (crow + 1) + 1 => range(x, y) = [x, x+1, ... , y-1]
                            for tcol in range(max(0, ccol - 1), min(cols, ccol + 2)):   # (ccol + 1) + 1 => range(x, y) = [x, x+1, ... , y-1]
                                tcell = (trow, tcol) 
                                if not current.has_cell(tcell):
                                    to_be_explored.append(current.extend(tcell))
        return valid_snakes
            
    def sort_words(self, sort=SORT_BY_SCORE, reverse=False):
        """
        Sort the found words according to the requested method,
        and return them as a list.

        :param str sort: the sort method
        :param bool reverse: if ``True`` reverse the order of the words
        :rtype: list of
        """
        if sort == self.SORT_BY_LENGTH:
            key = lambda x: (len(x[0]), x[1], x[0])
            rev = True
        elif sort == self.SORT_BY_START:
            key = lambda x: (x[2].start, x[1], x[0])
            rev = False
        elif sort == self.SORT_BY_END:
            key = lambda x: (x[2].end, x[1], x[0])
            rev = False
        else:
            key = lambda x: (x[1], -len(x[0]), x[0])
            rev = True
        reverse = not rev if reverse else rev
        return sorted([self.found[word] for word in self.found], key=key, reverse=reverse)



