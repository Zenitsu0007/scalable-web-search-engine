"""search server configuration."""
import pathlib

APPLICATION_ROOT = '/'
SERACH_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATABASE_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# Database file
DATABASE_FILENAME = DATABASE_ROOT/'var'/'search.sqlite3'
