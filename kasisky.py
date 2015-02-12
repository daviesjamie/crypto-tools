#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In polyalphabetic substitution ciphers where the substitution alphabets are chosen by the use of a
keyword (such as the Vigenère cipher), the Kasiski test allows a cryptanalyst to deduce the length
of the keyword. It involves looking for repeated segments of characters, calculating the distances
between them, and then deducing the key length from the greatest common divisor of these distances.

This is a tool for performing the Kasisky test, with options for manually specifying a segment of
text or automatically finding one. It can also calculate the greatest common divisor of the
distances found.
"""

from fractions import gcd
from frequency import word_frequency
from operator import itemgetter

import argparse
import re
import string
import sys


def get_all_indices(segment, text, case_sensitive=False):
    """Gets all the index of all occurences of a segment in a given text."""
    clean_text = ''
    for char in text:
        if char in string.ascii_letters:
            clean_text += char if case_sensitive else string.upper(char)

    return [m.start() for m in re.finditer(segment, clean_text)]


def get_distances_between(segment, text):
    """Gets the distances between all occurences of a segment in a given text."""
    indices = get_all_indices(segment, text)
    distances = []

    for i in range(1, len(indices)):
        distances.append(indices[i] - (indices[i-1] + len(segment)))

    return distances


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--auto', '-a', help='Automatically find a suitable repeated segment',
                        action='store_true', dest='auto', default=False)

    parser.add_argument('--auto-min-length', '-l',
                        help='Minimum length of repeated segment to find', action='store',
                        dest='min_length', default=3, type=int)

    parser.add_argument('--case-sensitive', help='Ignore case in input text', action='store_true',
                        dest='case_sensitive', default=False)

    parser.add_argument('--gcd', '-g',
                        help='Calculate the greatest common divisor (an estimate for the key length)',
                        action='store_true', dest='gcd', default=False)

    parser.add_argument('--segment', '-s', help='The repeated segment to search for',
                        action='store', dest='segment', default=None)

    args = parser.parse_args()
    stdin = sys.stdin.read()

    if args.segment:
        segment = args.segment
    else:
        segment = max(word_frequency(stdin, min_length=args.min_length, case_sensitive=args.case_sensitive).iteritems(), key=itemgetter(1))[0]

    print 'Using segment "{}"'.format(segment)

    distances = get_distances_between(segment, stdin)
    print '\n'.join(str(x) for x in distances)

    if args.gcd:
        print 'GCD: {}'.format(reduce(gcd, distances))

