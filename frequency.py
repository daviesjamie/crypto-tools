#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from operator import itemgetter

import string

MAX_WIDTH = 80
SEPARATOR = ' │ '
GRAPH_CHAR = '█'

def char_frequency(text, case_sensitive=False):
    counts = {}

    for char in text:
        if char not in string.ascii_letters:
            continue
        c = char if case_sensitive else string.lower(char)
        counts[c] = counts.get(c, 0) + 1

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
            line += str(val)
            line += ' ' * (val_str_max - len(str(val))) if len(str(val)) < val_str_max else ''

        if graph:
            line += SEPARATOR
            line += GRAPH_CHAR * int(round(val * scale))

        print line


if __name__ == '__main__':
    d = char_frequency('asdlfhaasdfjasdfkljhasd;kfasdfajsdfkajdf')
    pretty_output(d, counts=True, sort_by='val')
