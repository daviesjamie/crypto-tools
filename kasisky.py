#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fractions import gcd

import argparse
import re
import string
import sys


def get_all_indices(segment, text):
    clean_text = ''
    for char in text:
        if char in string.ascii_letters:
            clean_text += char

    return [m.start() for m in re.finditer(segment, clean_text)]


def get_distances_between(segment, text):
    indices = get_all_indices(segment, text)
    distances = []

    for i in range(1, len(indices)):
        distances.append(indices[i] - (indices[i-1] + len(segment)))

    return distances


if __name__ == '__main__':
    stdin = sys.stdin.read()

    parser = argparse.ArgumentParser()
    parser.add_argument('segment', help='The segment to search for', action='store')
    parser.add_argument('--gcd', '-g', help='Calculate the greatest common divisor (an estimate for the key length)', action='store_true', dest='gcd', default=False)

    args = parser.parse_args()
    distances = get_distances_between(args.segment, stdin)

    print '\n'.join(str(x) for x in distances)

    if args.gcd:
        print 'GCD: {}'.format(reduce(gcd, distances))

