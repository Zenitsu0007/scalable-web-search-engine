#!/usr/bin/env python3
"""Reduce 3: <tk, idfk, di, tfik>"""
import sys
import itertools
import math


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)

    with open("total_document_count.txt", "r", encoding="utf-8") as total:
        for line in total:
            n_doc = int(line.strip())

    nk = len(group)
    idfk = math.log(n_doc/nk, 10)
    for line in group:
        line = line.strip()
        _, rest = line.split("\t")
        print(f"{key} {idfk} {rest}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
