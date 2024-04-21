#!/usr/bin/env python3
"""Reduce 0: total_docs."""

import sys


def main():
    """Add file count."""
    total_docs = 0

    # Read each line from stdin (output of mapper)
    for line in sys.stdin:
        # Extract the key and the count
        _, count = line.strip().split()
        total_docs += int(count)

    # Output the total number of documents
    print(total_docs)


if __name__ == "__main__":
    main()
