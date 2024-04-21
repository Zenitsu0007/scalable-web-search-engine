#!/usr/bin/env python3
"""Reduce 5: <(tk, idfk), (di, tfik, normali), (dj, tfjk, normalj)...>."""
import sys
import itertools
from collections import defaultdict


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)

    output = key
    output = defaultdict(list)
    for line in group:
        line = line.strip()
        _, values = line.split("\t")
        tk, idfk, di, tfik, normal = values.split()
        dict_key = (tk, idfk)
        output[dict_key].append([di, tfik, normal])

    for term in output:
        final = term[0] + " " + term[1]
        for item in output[term]:
            item_list = " ".join(item)
            final = final + " " + item_list
        print(final)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
