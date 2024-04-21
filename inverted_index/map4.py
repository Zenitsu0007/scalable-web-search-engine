#!/usr/bin/env python3
"""Map 4: <di, (tk, idfk, tfik)>."""

import sys


for line in sys.stdin:
    line = line.strip()
    tk, idfk, di, tfik = line.split()
    print(f"{di}\t{tk} {idfk} {tfik}")
