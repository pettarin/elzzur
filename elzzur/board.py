#!/usr/bin/env python
# coding=utf-8

"""
A Ruzzle board.
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import os
import random

from elzzur.languages import LANGUAGES, LETTER_SCORE, LETTER_FREQUENCY

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

TRIPLE_WORD = "tw"
""" Triple word multiplier placeholder """

DOUBLE_WORD = "dw"
""" Double word multiplier placeholder """

TRIPLE_LETTER = "tl"
""" Triple letter multiplier placeholder """

DOUBLE_LETTER = "dl"
""" Double letter multiplier placeholder """

LENGTH_POINTS = {
    9: 25,
    8: 20,
    7: 15,
    6: 10,
    5: 5,
}
""" Length points """

MULTIPLIERS = {
    TRIPLE_WORD: (3, 1),
    DOUBLE_WORD: (2, 1),
    TRIPLE_LETTER: (1, 3),
    DOUBLE_LETTER: (1, 2),
}
""" Values of the multipliers """

MULTIPLIERS_CDF = [
    (TRIPLE_WORD, 0.05),    #  5%
    (DOUBLE_WORD, 0.15),    # 10%
    (TRIPLE_LETTER, 0.25),  # 10%
    (DOUBLE_LETTER, 0.40),  # 15%
    ("", 1.0)               # 60%
]
""" CDF of the multipliers, used for generating random boards """

class BoardCell(object):
    """
    A cell of the board.
    
    :param str token: the token, containing the letter (e.g., ``E``) and possibly its multiplier (e.g., ``Mtw`` or ``Adl``)
    :param str language: the language code (e.g. ``en``) of the board, used to determine the letter score
    """
    def __init__(self, token, language):
        self.letter = token[0].upper()
        if self.letter not in LETTER_SCORE[language]:
            raise ValueError("Unrecognized letter '%s' for language '%s'." % (token[0], language))
        self.word_multiplier = 1
        self.letter_multiplier = 1
        self.token_multiplier = ""
        if len(token) > 1:
            self.token_multiplier = token[1:].lower()
            if self.token_multiplier not in MULTIPLIERS:
                raise ValueError("Unrecognized multiplier '%s'." % (token[1:]))
            self.word_multiplier, self.letter_multiplier = MULTIPLIERS[self.token_multiplier]
        self.score = LETTER_SCORE[language][self.letter] * self.letter_multiplier

    def __str__(self):
        return u"%s (L=%d, W=%d)" % (self.letter, self.score, self.word_multiplier)

    def pretty_print(self, multiplier=False):
        """
        Pretty print the cell.

        :param bool multiplier: if ``True``, print the multiplier
        """
        if multiplier:
            return u"%s%s" % (self.letter, self.token_multiplier) 
        return u"%s" % self.letter

class Board(object):
    """
    A Ruzzle board.

    :param str language: the language code (e.g. ``en``) of the board, used to determine the letter score
    """
    def __init__(self, language):
        if language not in LETTER_SCORE:
            raise ValueError("No score available for the given language. (Got '%s')" % language)
        self.language = language
        self.cells = {}
        self.rows = 0
        self.cols = 0

    def __str__(self):
        acc = []
        for i in range(self.rows):
            acc.append(u" ".join([str(self.cells[(i, j)]) for j in range(self.cols)]))
        return u"\n".join(acc)

    def pretty_print(self, multipliers=False):
        """
        Pretty print the board.

        :param bool multipliers: if ``True``, print the multipliers
        :rtype: str
        """
        acc = []
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                letter = self.cells[(i, j)].pretty_print(multiplier=multipliers)
                padding = " " * (4 - len(letter))
                row += letter + padding
            acc.append(row)
        return u"\n".join(acc)

    @property
    def letters(self):
        """
        Return the list of letters in the board.

        :rtype: list of str
        """
        return [l.letter for l in list(self.cells.values())]

    def letter_at(self, cell):
        """
        Return the letter at the given cell.
        
        :param tuple cell: the ``(x, y)`` cell to be checked for
        """
        return self.cells[cell].letter

    def compute_snake_word(self, snake):
        """
        Return the word corresponding to the given snake.

        :param Snake snake: the snake corresponding to the desired word
        :rtype: str
        """
        return u"".join([self.cells[cell].letter for cell in snake.cells])

    def compute_snake_score(self, snake):
        """
        Return the score corresponding to the given snake.

        :param Snake snake: the snake corresponding to the desired word
        :rtype: int
        """
        acc = sum([self.cells[cell].score for cell in snake.cells])
        for cell in snake.cells:
            acc *= self.cells[cell].word_multiplier
        if len(snake) in LENGTH_POINTS:
            acc += LENGTH_POINTS[len(snake)]
        return acc

    def save_to_file(self, file_path):
        """
        Save the board to file.
        
        :param str file_path: the path of the output file to be written
        """
        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(self.pretty_print(multipliers=True))

    def read_board_file(self, file_path):
        """
        Read a plain text, UTF-8 encoded file,
        containing one line per board row,
        with letters separated by one or more spaces.

        Example::

            Ttl R   S Ndl
            Odw Htw E I
            Cdw I   N V
            Etl A   D E


        :param str file_path: the path of the input file to be read
        :rtype: Board
        """
        if not os.path.isfile(file_path):
            raise IOError("The board file does not exist. (Got: '%s')" % file_path)
        self.cells = {}
        row = 0
        cols = []
        with io.open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if len(line.strip()) == 0:
                    break
                col = 0
                for t in [l for l in line.strip().split(" ") if len(l) > 0]:
                    self.cells[(row, col)] = BoardCell(t, self.language)
                    col += 1
                cols.append(col)
                row += 1
        # check that we have at least one row
        if row < 1:
            raise ValueError("The board file seems empty.")
        # check that all rows have the same number of columns
        for j in range(len(cols) - 1):
            if cols[j] != cols[j+1]:
                raise ValueError("The board file has two rows with a different number of columns. (Got: row %d has %d cols while row %d had %d cols))" % (j, cols[j], j+1, cols[j+1]))
        # all good, store the number of rows and columns
        self.rows = row
        self.cols = cols[0]
        return self

    def generate_random_board(self, rows=4, cols=4):
        """
        Generate a random board.

        :param int rows: the number of rows of the desired board
        :param int cols: the number of columns of the desired board
        :rtype: Board
        """
        def cumsum(letter_freq):
            # numpy has cumsum, but I do not want numpy as dependency
            cum_freq = []
            f_prev = 0.0
            for (l, f) in letter_freq:
                f_prev += f
                cum_freq.append((l, f_prev))
            f_sum = cum_freq[-1][1]
            return [(l, f/f_sum) for (l, f) in cum_freq]

        def draw_from_distribution(cdf):
            #
            # numpy has digitize() and numpy.random, but I do not want numpy as dependency
            # this can be done with binary search instead of linear search
            #
            # in general, one should use the distribution of N-grams, N>=2 instead of single letter frequencies (N=1)
            # I suspect that the original Ruzzle builds the board so that there are at least M words, etc.
            # (i.e., the boards are not truly "random", based on some N-gram distribution)
            #
            rnd = random.uniform(0, 1)
            for (element, cf) in cdf:
                if rnd <= cf:
                    return element

        self.cells = {}
        self.rows = rows
        self.cols = cols
        sorted_letters = sorted([(l, LETTER_FREQUENCY[self.language][l]) for l in LETTER_FREQUENCY[self.language]])
        cum_freq = cumsum(sorted_letters)
        for row in range(self.rows):
            for col in range(self.cols):
                letter = draw_from_distribution(cum_freq)
                multiplier = draw_from_distribution(MULTIPLIERS_CDF)
                self.cells[(row, col)] = BoardCell(letter + multiplier, self.language)
        return self



