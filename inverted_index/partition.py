#!/usr/bin/env -S python3 -u
"""Partition into segments."""
import sys


for line in sys.stdin:
    key, _, _ = line.partition("\t")
    print(int(key))
