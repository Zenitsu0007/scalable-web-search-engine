"""REST API for index."""
import hashlib
import flask
import index


@index.app.route('/api/v1/')
def get_index():
    """Return a list of services available."""
    context={"hits": "/api/v1/hits/", "url": "/api/v1/"}
    return flask.jsonify(**context), 200


@index.app.route('/api/v1/hits/')
def hits():
    """Return a list of hits with doc ID and score."""
    query=flask.request.args.get('q')
    weight=flask.request.args.get('w',0.5)
    context ={"hits":[]}
    return flask.jsonify(**context), 200