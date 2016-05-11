# elzzur

**elzzur** solves a Ruzzle board, listing all the valid words with their scores.

* Version: 0.0.1
* Date: 2016-05-11
* Developer: [Alberto Pettarin](http://www.albertopettarin.it/)
* License: the MIT License (MIT)
* Contact: [click here](http://www.albertopettarin.it/contact.html)

## Usage

```
$ python -m elzzur --help
$ python -m elzzur solve -l language -b board [-d dictionary] [OPTIONS] 
$ python -m elzzur demo -l language 
$ python -m elzzur languages 
$ python -m elzzur cat -d dictionary [-o output]
$ python -m elzzur compile -d dictionary -o output
$ python -m elzzur generate -l language [-r rows] [-c columns] [-o board]
```

In demo mode elzzur will solve a built-in real board for the given language.

If you do not specify a dictionary file,
the built-in dictionary for the given language will be used.

## Examples

```bash
$ python -m elzzur demo  -l en 
$ python -m elzzur solve -l en -b /path/to/en.board 
$ python -m elzzur solve -l en -b /path/to/en.board -d /path/to/your.dict.txt
$ python -m elzzur solve -l it -b /path/to/it.board -d /path/to/your.dict.marisa 
```

Output (board, list of words, statistics):

```bash
$ python -m elzzur demo  -l en

Ttl R   S   Ndl 
Odw Htw E   I   
Cdw I   N   V   
Etl A   D   E   

COHESIVE    224    (2,0) (1,0) (1,1) (1,2) (0,2) (1,3) (2,3) (3,3)
HEROIC      154    (1,1) (1,2) (0,1) (1,0) (2,1) (2,0)
CHORES      154    (2,0) (1,1) (1,0) (0,1) (1,2) (0,2)
COHEN       149    (2,0) (1,0) (1,1) (1,2) (0,3)
ECHO        144    (3,0) (2,0) (1,1) (1,0)
...
IA          2      (2,1) (3,1)
ES          2      (1,2) (0,2)
ER          2      (1,2) (0,1)
AN          2      (3,1) (2,2)
AI          2      (3,1) (2,1)

Number of words:            281
Length of the longest word: 8
Maximum total score:        7376
```

See the [OUTPUT file](OUTPUT.md) for the full output.

## Installation

```bash
$ pip install elzzur
```

or

```bash
$ git clone https://github.com/pettarin/elzzur
$ cd elzzur
$ python setup.py install
```

You need the ``marisa-trie`` Python package to run elzzur (``pip install marisa-trie``).

## Scoring Rules

1. Only words in the given dictionary are valid.
2. Only words at least two letters long are valid.
3. A snake (i.e., a sequence of adjacent letters) cannot intersect itself, that is, each board cell can be used at most once per snake.
4. Only one snake per word counts, that is, only the first snake forming a word will get points.
5. The score of a snake is the sum of the scores of its letters (each multiplied by its letter multiplier, if any), times the product of the word multipliers (if any), plus the word length points.
6. The word length points are: 25 for 9-letter words, 20 for 8, 15 for 7, 10 for 6, 5 for 5, 0 for all the other cases.

## Available Languages

The following languages are supported, which means that the code includes
a sample board, letter score, and letter frequency for each of them:

* ``de``
* ``en``
* ``es``
* ``fr`` (letter score TBC)
* ``it``
* ``nl``
* ``pt`` (letter score TBC)

### Adding A New Language

You need to modify the ``elzzur/languages.py``.
Specifically, you need to edit the following constants:

1. ``LANGUAGES``: add your language code, say ``zz``;
2. ``LETTER_SCORE``: add the score of each letter for language ``zz``;
3. ``LETTER_FREQUENCY``: add the frequency of each letter in language ``zz``, normalizing Unicode and case.

You should also provide a real board file ``zz.board``,
and the ``zz.marisa`` dictionary derived from ``aspell-zz``.

If you add a new language, please open a pull request, so that everyone can get it!

## Dictionary File Format

The dictionary file must be a plain text,
UTF-8 encoded file,
with one word per line:

```
a
A
AA
AAA
Aachen
aah
Aaliyah
...
```

The words will undergo [Unicode NFKD](http://unicode.org/reports/tr15/)
and [case normalization](http://unicode.org/faq/casemap_charprop.html),
resulting in a dictionary of (uppercased) ASCII words.
For example, the Italian word ``caffè`` (coffee) will become ``CAFFE``.

Alternatively, dictionary files can be compiled MARISA files,
which are binary serializations of MARISA tries
(see Section [Solver Strategy](#solver-strategy) for details).
Providing the dictionary in this format will make the loading time shorter.
To compile a plain text dictionary into a MARISA binary dictionary,
you can invoke:

```
$ python -m elzzur compile -d /path/to/plain/dictionary -o /path/to/output.marisa
```

Please note that you need to specify the ``.marisa`` extension for elzzur
to load the file as a MARISA trie.
Otherwise, it will try to read it as a plain text file, failing.

## Board File Format

The board file must be an ASCII file,
containing one line per board row,
with letters separated by one space
(or more, as multiple spaces are counted as one),
for example:

```
Ttl R   S Ndl
Odw Htw E I
Cdw I   N V
Etl A   D E
```

The board can have dimensions ``NxM``, with ``N >= 1, M >= 1``, not just ``4x4``,
under the constraint that all the rows must have the same number of columns (letters),
that is, the board cannot contain holes.

The multipliers, if present, must be appended to the corresponding letter, using the following codes:

* ``tw``: triples the value of the word
* ``dw``: doubles the value of the word
* ``tl``: triples the value of the letter
* ``dl``: doubles the value of the letter

You can generate a random board with:

```
$ python -m elzzur generate -l language [-r rows] [-c cols] [-o outputfile]
```

## Solver Strategy

The current implementation solves a given board in three steps:

1. it finds all the valid snakes, that is, all the adjacent sequences of letters corresponding to a valid word in the dictionary;
2. for each word, it keeps only the snake with the highest score; and
3. it sorts the words (and the corresponding highest scoring snake), according to the method requested by the user: score, word length, word start cell, word end cell.

To find all the valid snakes, a BFS exploration of the board is performed (simulated with a queue),
avoiding extending the current snake if either:

1. the snake will self-intersect or,
2. the word corresponding to the current snake is not a prefix of any word in the dictionary.

Clearly, the crucial point consists in speeding the prefix testing up.
Hence, the dictionary is stored in memory as a MARISA trie
(either loaded from a serialized trie version, or converted from a plain text file).

A [MARISA trie](http://s-yata.github.io/marisa-trie/docs/readme.en.html) is a very efficient trie (prefix tree),
in terms of both storage space and preprocessing/running time.
In particular, it guarantees that the following operations are extremely fast:

1. ``has_keys_with_prefix(prefix)``
2. ``keys_with_prefix(prefix)``
3. ``has_key(key)``

The [Python module](https://pypi.python.org/pypi/marisa-trie) ``marisa-trie``
is based on the [original C++](https://github.com/s-yata/marisa-trie) MARISA code.

Currently, elzzur can solve a 4x4 board in less than 100ms, and a 10x10 board in about 5s.

## TODO List

* Let the user run with a new language without editing the source code
* Let the user alter the letter scores without editing the source code
* Let the user specify the letter scores directly in the board file
* Some languages have letters other than ``A-Z``
* Generalize the game to be case-sensitive
* Generalize the game to allow self-intersecting snakes
* Generalize the game to allow holes in the board
* Better random board generation, e.g. based on N-grams and/or vocabulary
* Given a board (hence, the letters and their number of repetitions), one can prune the dictionary trie, excluding words that cannot be formed with the given available letters
* Confirm letter scores for ``fr`` and ``pt``
* Confirm length points for words longer than 9 letters
* Define rules and scores outside the code, using some format/lib TBD
* Nicer command line interface, e.g. better argparse and examples

## License

**elzzur** is released under the MIT License.

The included MARISA dictionaries ``res/*.marisa``
were compiled from the corresponding [GNU aspell](http://aspell.net/) dictionaries,
and they are released under the same license,
that is, the GNU GPL v2 License, see the [licenses](licenses) directory.

[Ruzzle](http://ruzzle-game.com/) is a product of MAG Interactive(TM).

## Acknowledgments

* My sister and nephews for introducing me to Ruzzle



