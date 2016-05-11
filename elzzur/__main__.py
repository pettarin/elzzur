#!/usr/bin/env python
# coding=utf-8

"""
elzzur solves a Ruzzle board, listing all the valid words with their scores.

This is the main elzzur script, intended to be run from command line.
"""

from __future__ import absolute_import
from __future__ import print_function
import argparse
import os
import sys

from elzzur.board import Board 
from elzzur.languages import LANGUAGES
from elzzur.mtdictionary import MTDictionary
from elzzur.solver import Solver

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

DESCRIPTION = "elzzur solves a Ruzzle board"

ARGUMENTS = [
    {
        "long": "command",
        "short": None,
        "nargs": None,
        "type": str,
        "default": None,
        "help": "[cat|compile|demo|generate|languages|solve]"
    },
    {
        "long": "--language",
        "short": "-l",
        "nargs": "?",
        "type": str,
        "default": None,
        "help": "Language code (e.g., 'en')"
    },
    {
        "long": "--dictionary",
        "short": "-d",
        "nargs": "?",
        "type": str,
        "default": None,
        "help": "Path to the dictionary file"
    },
    {
        "long": "--board",
        "short": "-b",
        "nargs": "?",
        "type": str,
        "default": None,
        "help": "Path to the board file"
    },
    {
        "long": "--output",
        "short": "-o",
        "nargs": "?",
        "type": str,
        "default": None,
        "help": "Path to the output file"
    },
    {
        "long": "--rows",
        "short": "-r",
        "nargs": "?",
        "type": int,
        "default": 4,
        "help": "The number of rows of the board to generate"
    },
    {
        "long": "--cols",
        "short": "-c",
        "nargs": "?",
        "type": int,
        "default": 4,
        "help": "The number of columns of the board to generate"
    },
    {
        "long": "--sort",
        "short": "-s",
        "nargs": "?",
        "type": str,
        "default": "score",
        "help": "Sort words by [score|length|start|end]"
    },
    {
        "long": "--reverse",
        "short": "-R",
        "action": "store_true",
        "help": "Reverse the list of words"
    },
    {
        "long": "--quiet",
        "short": "-q",
        "action": "store_true",
        "help": "Do not output board and statistics"
    },
]

def print_error(msg):
    """
    Print the given error message and exit.

    :param str msg: the error message
    """
    print(msg)
    sys.exit(1)

def check_language(vargs):
    """
    Check that the language has been specified,
    and that it is among the supported ones.
    On error, print error message and exit. 

    :param dict vargs: the command line arguments
    """
    if vargs["language"] is None:
        print_error("You must specify the language of the board.")
    if vargs["language"] not in LANGUAGES:
        print_error("You must specify a supported language: %s" % ", ".join(LANGUAGES))

def list_languages():
    """
    List all the available languages
    """
    print("Supported languages: %s" % ", ".join(LANGUAGES))

def demo_mode(vargs):
    """
    Solve a built-in board.
    
    :param dict vargs: the command line arguments
    """
    check_language(vargs)
    vargs["board"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "res/" + vargs["language"] + ".board"))
    solve_board(vargs)

def solve_board(vargs):
    """
    Solve a board.
    
    :param dict vargs: the command line arguments
    """
    check_language(vargs)
    if vargs["board"] is None:
        print_error("You must specify the path of the board file to solve.")
    if vargs["dictionary"] is None:
        vargs["dictionary"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "res/" + vargs["language"] + ".marisa"))
    dictionary = MTDictionary(vargs["dictionary"], normalize=True, ignore_case=True)
    board = Board(vargs["language"]).read_board_file(vargs["board"])
    if not vargs["quiet"]:
        print("")
        print(board.pretty_print(multipliers=True))
        print("")
    solver = Solver(board, dictionary)
    words = solver.solve(sort=vargs["sort"], reverse=vargs["reverse"])
    length_longest_word = max([len(w[0]) for w in words])
    length_max_score = len(str(max([w[1] for w in words])))
    total = 0
    for (word, snake_score, snake) in words:
        word_padding = " " * (length_longest_word - len(word))
        score_padding = " " * (length_max_score - len(str(snake_score)))
        print("%s%s    %d%s    %s" % (word, word_padding, snake_score, score_padding, snake))
        total += snake_score
    if not vargs["quiet"]:
        print("")
        print("Number of words:            %d" % len(words))
        print("Length of the longest word: %d" % length_longest_word)
        print("Maximum total score:        %d" % total)
        print("")

def generate_board(vargs):
    """
    Generate a random board.
    
    :param dict vargs: the command line arguments
    """
    check_language(vargs)
    board = Board(vargs["language"]).generate_random_board(rows=vargs["rows"], cols=vargs["cols"])
    print(board.pretty_print(multipliers=True))
    if vargs["output"] is not None:
        board.save_to_file(vargs["output"])
        print("")
        print("File '%s' saved" % vargs["output"])

def cat_dictionary(vargs):
    """
    Output the keys in the given dictionary to stdout.
    No normalization will take place!
    
    :param dict vargs: the command line arguments
    """
    if vargs["dictionary"] is None:
        print_error("You must specify the path of the input dictionary file.")
    words = MTDictionary(vargs["dictionary"], normalize=False, ignore_case=False)
    if vargs["output"] is not None:
        words.save_plain_text(vargs["output"])
        print("File '%s' saved" % vargs["output"])
    else:
        for word in words.keys:
            print(word)

def compile_dictionary(vargs):
    """
    Compile the given dictionary into a MARISA trie,
    and save it to file.
    
    :param dict vargs: the command line arguments
    """
    if vargs["dictionary"] is None:
        print_error("You must specify the path of the input dictionary file.")
    if vargs["output"] is None:
        print_error("You must specify the path of the output dictionary file.")
    output_file_path = vargs["output"]
    if not output_file_path.endswith(".marisa"):
        output_file_path += ".marisa"
    words = MTDictionary(vargs["dictionary"], normalize=True, ignore_case=True)
    words.save_marisa_trie(output_file_path)
    print("File '%s' saved" % output_file_path)

def main():
    """
    Entry point.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    for arg in ARGUMENTS:
        if "action" in arg:
            if arg["short"] is not None:
                parser.add_argument(arg["short"], arg["long"], action=arg["action"], help=arg["help"])
            else:
                parser.add_argument(arg["long"], action=arg["action"], help=arg["help"])
        else:
            if arg["short"] is not None:
                parser.add_argument(arg["short"], arg["long"], nargs=arg["nargs"], type=arg["type"], default=arg["default"], help=arg["help"])
            else:
                parser.add_argument(arg["long"], nargs=arg["nargs"], type=arg["type"], default=arg["default"], help=arg["help"])
    vargs = vars(parser.parse_args())
    command = vargs["command"]
    if command == "languages":
        list_languages()
    elif command == "demo":
        demo_mode(vargs)
    elif command == "solve":
        solve_board(vargs)
    elif command == "generate":
        generate_board(vargs)
    elif command == "cat":
        cat_dictionary(vargs)
    elif command == "compile":
        compile_dictionary(vargs)
    else:
        parser.print_help()
        sys.exit(2)
    sys.exit(0)



if __name__ == "__main__":
    main()



