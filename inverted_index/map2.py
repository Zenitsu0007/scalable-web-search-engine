#!/usr/bin/env python3
"""Map 2: <(tk, di), 1>."""

import sys


INCREMENT = 1

for line in sys.stdin:
    line = line.strip()
    doc_id, content = line.split("\t")
    terms = content.split()
    for term in terms:
        print(f"{term} {doc_id}\t{INCREMENT}")
