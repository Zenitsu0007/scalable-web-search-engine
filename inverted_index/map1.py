#!/usr/bin/env python3
"""Map 1: Extract text from HTML and compute a unique document ID."""

import sys
import hashlib
import re
import bs4


ALGORITHM = 'sha512'

def clean_text(text, stopwords):
    """Clean text and remove stop words."""
    # Remove non-alphanumeric characters that also aren’t spaces
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    # Convert upper case characters to lower case
    text = text.casefold()
    # Split the text into whitespace-delimited terms
    words = text.split()
    # Remove stopwords
    words = [word for word in words if word not in stopwords]
    return ' '.join(words)

stops = set()
with open("stopwords.txt", "r", encoding="utf-8") as stopwords_file:
    for line in stopwords_file:
        stops.add(line.strip())

# Parse one HTML document at a time.  Note that this is still O(1) memory
# WRT the number of documents in the dataset.
HTML = ""
for line in sys.stdin:
    # Assume well-formed HTML docs:
    # - Starts with <!DOCTYPE html>
    # - End with </html>
    # - Contains a trailing newline
    if "<!DOCTYPE html>" in line:
        HTML = line
    else:
        HTML += line

    # If we're at the end of a document, parse
    if "</html>" not in line:
        continue

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(HTML, "html.parser")

    # Parse content from document
    # get_text() will strip extra whitespace and
    # concatenate content, separated by spaces
    element = soup.find("html")
    content = element.get_text(separator=" ", strip=True)
    # Remove extra newlines
    content = content.replace("\n", "")

    # Calculate doc_id by hashing the document content
    hash_obj = hashlib.new(ALGORITHM)
    hash_obj.update(content.encode("utf-8"))
    doc_id = hash_obj.hexdigest()
    # Mod by 10^7 to limit the length of the doc_id
    doc_id = int(doc_id, 16) % (10**7)

    # Emit one line for each document, including the doc ID and document content
    print(f"{doc_id}\t{clean_text(content, stops)}")

    # Reset HTML for the next document
    HTML = ""
