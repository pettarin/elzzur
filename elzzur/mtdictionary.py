#!/usr/bin/env python
# coding=utf-8

"""
A dictionary based on MARISA trie.

This implementation requires the ``marisa-trie`` Python package (``pip install marisa-trie``).
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import marisa_trie
import os
import unicodedata

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

class MTDictionary(object):
    """
    A dictionary based on a MARISA trie.

    A trie (a.k.a. prefix tree) dictionary allows for very fast checking
    if there are words in the dictionary starting with a given prefix,
    and, if so, to retrieve them all.

    MARISA is a very efficient trie implementation.

    This class allows reading a dictionary from
    a. a MARISA file, or
    b. a plain text, UTF-8 encoded file.
    In the latter case, you can save the resulting MARISA trie to file to use it later.

    :param str dictionary_file_path: path to the dictionary file to read. If it ends with ``.marisa``, it is read as a MARISA trie.
    :param bool normalize: if ``True``, apply Unicode NFKD + decode to ascii to the dictionary entries
    :param bool ignore_case: if ``True``, ignore case, that is, make all dictionary entries uppercase
    """
    def __init__(self, dictionary_file_path, normalize=False, ignore_case=False):
        if not os.path.isfile(dictionary_file_path):
            raise IOError("The dictionary file does not exist. (Got: '%s')" % dictionary_file_path)
        if dictionary_file_path.endswith(".marisa"):
            self.read_marisa_file(dictionary_file_path)
        else:
            self.read_plain_file(dictionary_file_path, normalize=normalize, ignore_case=ignore_case)

    def __len__(self):
        return len(self.trie)

    @property
    def keys(self):
        """
        Return the sorted list of keys in the dictionary.

        :rtype: list of str
        """
        return sorted([w for w in self.trie])

    def has_key(self, key):
        """
        Return ``True`` if the given key is present in the dictionary.

        :param str key: the key (word) to be checked for
        :rtype: bool
        """
        return key in self.trie

    def has_keys_with_prefix(self, prefix):
        """
        Return ``True`` if in the dictionary there are keys with the given prefix.

        :param str key: the prefix (word prefix) to be checked for
        :rtype: bool
        """
        return self.trie.has_keys_with_prefix(prefix)

    def keys_with_prefix(self, prefix):
        """
        Return a list of keys in the dictionary with the given prefix.

        :param str key: the prefix (word prefix) to be checked for
        :rtype: list of str
        """
        return self.trie.keys(prefix)

    def read_marisa_file(self, file_path):
        """
        Read a MARISA trie from file and return it.

        :param str file_path: the path of the input file to be read
        """
        self.trie = marisa_trie.Trie()
        with io.open(file_path, "rb") as f:
            self.trie.read(f)

    def read_plain_file(self, file_path, normalize=False, ignore_case=False):
        """
        Read a plain text, UTF-8 encoded file,
        containing one word per line,
        and return a MARISA trie from it.
        
        :param str file_path: the path of the input file to be read
        :param bool normalize: if ``True``, apply Unicode NFKD + decode to ascii to the dictionary entries
        :param bool ignore_case: if ``True``, ignore case, that is, make all dictionary entries uppercase
        """
        with io.open(file_path, "r", encoding="utf-8") as f:
            dictionary = f.read()
        if normalize:
            dictionary = unicodedata.normalize("NFKD", dictionary).encode("ascii", "ignore")
        if ignore_case:
            dictionary = dictionary.upper()
        words = []
        for line in dictionary.split(u"\n"):
            words.append(line.strip())
        self.trie = marisa_trie.Trie(words)

    def save_marisa_trie(self, file_path):
        """
        Save the MARISA trie to file.
        
        :param str file_path: the path of the output file to be written
        """
        with io.open(file_path, "wb") as f:
            self.trie.write(f)

    def save_plain_text(self, file_path):
        """
        Save the dictionary to file as plain text.
        
        :param str file_path: the path of the output file to be written
        """
        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(u"\n".join(self.keys))



