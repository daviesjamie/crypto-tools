#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from operator import itemgetter

import argparse
import string
import sys

MAX_WIDTH = 80
SEPARATOR = ' │ '
GRAPH_CHAR = '█'


def char_frequency(text, case_sensitive=False):
    counts = {}

    for char in text:
        if char not in string.ascii_letters:
            continue
        c = char if case_sensitive else string.upper(char)
        counts[c] = counts.get(c, 0) + 1

    return counts


def ngram_frequency(text, n, case_sensitive=False):
    counts = {}
    ngram = ''

    for char in text:
        if char not in string.ascii_letters:
            ngram = ''
            continue

        ngram += char if case_sensitive else string.upper(char)

        if len(ngram) == n:
            counts[ngram] = counts.get(ngram, 0) + 1
            ngram = ngram[1:]

    return counts


def word_frequency(text, min_length=1, case_sensitive=False):
    counts = {}
    word = ''

    for char in text:
        if char not in string.ascii_letters:
            if len(word) >= min_length:
                counts[word] = counts.get(word, 0) + 1
            word = ''
            continue

        word += char if case_sensitive else string.upper(char)

    return counts


def pretty_output(data, sort_by='key', counts=True, graph=True):
    if sort_by == 'key':
        data = OrderedDict(sorted(data.items(), key=itemgetter(0)))
    elif sort_by == 'val':
        data = OrderedDict(sorted(data.items(), key=itemgetter(1), reverse=True))

    key_str_max = 0
    val_str_max = 0
    val_int_max = 0

    for key, val in data.iteritems():
        key_str_max = max(key_str_max, len(str(key)))
        val_str_max = max(val_str_max, len(str(val)))
        val_int_max = max(val_int_max, val)

    space_taken = key_str_max + len(SEPARATOR)
    space_taken += val_str_max + len(SEPARATOR) if counts else 0
    graph_max = MAX_WIDTH - space_taken

    scale = 1 if val_int_max < graph_max else graph_max / float(val_int_max)

    for key, val in data.iteritems():
        line = str(key)
        line += ' ' * (key_str_max - len(str(key))) if len(str(key)) < key_str_max else ''

        if counts:
            line += SEPARATOR
            line += ' ' * (val_str_max - len(str(val))) if len(str(val)) < val_str_max else ''
            line += str(val)

        if graph:
            line += SEPARATOR
            line += GRAPH_CHAR * int(round(val * scale))

        print line


if __name__ == '__main__':
    stdin = sys.stdin.read()

    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', '-g', help='Draw ascii histogram graph', action='store_true', dest='graph', default=False)
    parser.add_argument('--count', '-c', help='Output the count totals', action='store_true', dest='counts', default=False)
    parser.add_argument('--sort-by', '-s', help='Sort output by "key" or "val"', action='store', dest='sort_by', default='key')
    parser.add_argument('--case-sensitive', help='Make counting operations case sensitive', action='store_true', dest='case_sensitive', default=False)
    parser.add_argument('--ngram', '-n', help='Count ngrams of specified length', action='store', dest='ngram', default=None, type=int)
    parser.add_argument('--word', '-w', help='Count words of specified minimum length', action='store', dest='word', default=None, type=int)

    args = parser.parse_args()

    if args.ngram:
        char_counts = ngram_frequency(stdin, args.ngram, case_sensitive=args.case_sensitive)
    elif args.word:
        char_counts = word_frequency(stdin, min_length=args.word, case_sensitive=args.case_sensitive)
    else:
        char_counts = char_frequency(stdin, case_sensitive=args.case_sensitive)

    pretty_output(char_counts, sort_by=args.sort_by, counts=args.counts, graph=args.graph)

