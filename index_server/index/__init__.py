"""Initialize index server."""
import os
from pathlib import Path
import flask

app = flask.Flask(__name__)
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
app.config["PATH"] = str(Path(__file__).resolve().parent)

from index.api import load_index  # noqa: E402  pylint: disable=wrong-import-position

# Load inverted index, stopwords, and pagerank into memory
load_index.load_index()
