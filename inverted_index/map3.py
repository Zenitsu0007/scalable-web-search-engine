#!/usr/bin/env python3
"""Map 3: <tk, (di, tfik)>."""

import sys


for line in sys.stdin:
    line = line.strip()
    parts, tfik = line.split("\t")
    tk, di = parts.split()
    print(f"{tk}\t{di} {tfik}")
