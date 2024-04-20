#!/usr/bin/env python3
"""Map 0: <"doc", 1>"""

import sys
import re

INCREMENT = 1

# Pattern to find the <!DOCTYPE html> tag
doc_type_pattern = re.compile(r"<!DOCTYPE html>", re.IGNORECASE)

# Read each line from stdin (input)
for line in sys.stdin:
    # Check if the <!DOCTYPE html> tag is in the line
    if doc_type_pattern.search(line):
        # Emit a count of 1 for each document found
        print(f"doc\t{INCREMENT}")
