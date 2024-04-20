"""Search server model."""
import sqlite3
import flask
from flask import g
import search

def dict_factory(cursor, row):
    """
    Convert database row objects to a dictionary keyed on column name.
    This function is used to set the row factory, making it easier to work
    with SQLite query results.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_db():
    """
    Open a new database connection if there is none yet for the
    current application context.
    """
    if 'sqlite_db' not in g:
        # Assuming the database filename is stored in the app config
        db_filename = search.app.config['DATABASE_FILENAME']
        g.sqlite_db = sqlite3.connect(db_filename)
        g.sqlite_db.row_factory = dict_factory
        g.sqlite_db.execute("PRAGMA foreign_keys = ON")  # Enforce foreign-key constraints
    return g.sqlite_db

def close_db(e=None):
    """
    Close the current SQLite database connection.
    This function is typically called at the end of a request.
    """
    db = g.pop('sqlite_db', None)
    if db is not None:
        if e is None:
            db.commit()
        else:
            db.rollback()
        db.close()

def query_db(query, args=(), one=False):
    """
    Run a SQL query against the database and return the results.
    Args:
        query (str): SQL query to execute.
        args (tuple): arguments to bind to the query.
        one (bool): Return only the first result.
    Returns:
        List[dict]: A list of dictionaries representing the query result.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@search.app.teardown_appcontext
def teardown_db(exception):
    """
    Ensures that the database connection is closed when the app context is destroyed.
    Registered via the teardown_appcontext decorator to automatically be called.
    """
    if exception:
        close_db(exception)
    else:
        close_db()