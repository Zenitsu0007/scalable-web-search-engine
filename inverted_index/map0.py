#!/usr/bin/env python3
"""Map 0: Read input and mark file count."""

import sys
import re


# Pattern to find the <!DOCTYPE html> tag
doc_type_pattern = re.compile(r"<!DOCTYPE html>", re.IGNORECASE)

# Read each line from stdin (input)
for line in sys.stdin:
    # Check if the <!DOCTYPE html> tag is in the line
    if doc_type_pattern.search(line):
        # Emit a count of 1 for each document found
        print("doc", 1)
