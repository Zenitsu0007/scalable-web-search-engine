"""REST API for index."""
import math
import re
import flask
import index
from .load_index import stopwords, pagerank, inverted_index


@index.app.route('/api/v1/')
def get_index():
    """Return a list of services available."""
    context = {"hits": "/api/v1/hits/", "url": "/api/v1/"}
    return flask.jsonify(**context), 200


@index.app.route('/api/v1/hits/')
def get_hits():
    """Return a list of hits with doc ID and score."""
    query = flask.request.args.get('q')
    weight = float(flask.request.args.get('w', 0.5))
    qterm_freq = {}
    hits = []
    # cleaning query
    query = query.casefold()
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    for term in query.split():
        if term not in stopwords:
            if term not in qterm_freq:
                qterm_freq[term] = 1
                continue
            qterm_freq[term] += 1
    # find docs contianing every word in the cleaned query
    doc_id_set = []
    try:
        for term in qterm_freq:
            doc_id_set.append(set(inverted_index[term]['doc_info']))
        doc_id_set = set.intersection(*doc_id_set)
    except KeyError:
        # term not in index
        context = {"hits": []}
        return flask.jsonify(**context), 200
    # calculate score
    if doc_id_set and qterm_freq:
        # query vector
        query_vector = []
        for term, freq in qterm_freq.items():
            query_vector.append(inverted_index[term]['idf'] * freq)
        q_norm = math.sqrt(sum(x ** 2 for x in query_vector))
        # cal score for each doc
        for doc_id in doc_id_set:
            doc_vector = []
            for term in qterm_freq:
                doc_vector.append(inverted_index[term]['idf'] * inverted_index
                                  [term]['doc_info'][doc_id]['term_freq'])
            d_norm = math.sqrt(inverted_index[term]['doc_info']
                               [doc_id]['norm_factor'])
            tf_idf = sum(query_vector[i] * doc_vector[i]
                         for i in range(len(doc_vector))) / (q_norm * d_norm)
            weight_score = weight * pagerank[doc_id] + (1 - weight) * tf_idf
            hits.append({"docid": doc_id, "score": weight_score})
        hits.sort(key=lambda hit: (hit['score'],
                                   -1 * hit['docid']), reverse=True)
    context = {"hits": hits}
    return flask.jsonify(**context), 200
