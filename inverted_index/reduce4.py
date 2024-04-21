#!/usr/bin/env python3
"""Reduce 4: <di, normal, tk, idfk, tfik>."""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)

    normal = 0
    for line in group:
        line = line.strip()
        _, values = line.split("\t")
        tk, idfk, tfik = values.split()
        wik = float(tfik) * float(idfk)
        normal += (float(wik) * float(wik))

    for line in group:
        line = line.strip()
        _, values = line.split("\t")
        tk, idfk, tfik = values.split()
        print(f"{key} {normal} {tk} {idfk} {tfik}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
