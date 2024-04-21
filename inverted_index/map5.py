#!/usr/bin/env python3
"""Map 5: <di % 3, (tk, idfk, di, tfik, normal)>."""

import sys


for line in sys.stdin:
    line = line.strip()
    di, normal, tk, idfk, tfik = line.split()
    di3 = int(di) % 3
    print(f"{di3}\t{tk} {idfk} {di} {tfik} {normal}")
