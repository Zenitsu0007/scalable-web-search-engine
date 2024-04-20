"""Public Index Server tests."""
import utils


def test_multiple_terms(index_client):
    """Multiple word query.

    The PageRank weight parameter 'w' is missing.  The default value 0.5 should
    be used by the Index Server.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html

    """
    # Query the REST API
    response = index_client.get("/api/v1/hits/?q=water+bottle")
    assert response.status_code == 200

    # Compare actual hits to solution hits
    hits_actual = response.get_json()["hits"]
    hits_solution = [
        {
            "docid": 6910204,
            "score": 0.007634357212279204
        },
        {
            "docid": 4605259,
            "score": 0.006234000058455676
        },
        {
            "docid": 895525,
            "score": 0.003910411977743575
        },
        {
            "docid": 4068544,
            "score": 0.0032919912995216616
        },
        {
            "docid": 8278069,
            "score": 0.0030210521823423476
        },
        {
            "docid": 4658494,
            "score": 0.0020891903431959173
        }
    ]
    utils.assert_rest_api_hit_eq(hits_actual, hits_solution)


def test_special_characters(index_client):
    """Special characters in query.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Query the REST API
    response = index_client.get(
        "/api/v1/hits/?q=the+^most+apache+@@had@@oop&w=0"
    )
    assert response.status_code == 200

    # Compare actual hits to solution hits
    hits_actual = response.get_json()["hits"]
    hits_solution = [
        {
            "docid": 6415471,
            "score": 0.21667495788863178
        },
        {
            "docid": 3133315,
            "score": 0.06738653303975232
        },
        {
            "docid": 8803912,
            "score": 0.03924084932607922
        },
        {
            "docid": 8779462,
            "score": 0.027504285343936154
        },
        {
            "docid": 28594,
            "score": 0.024636547437612663
        },
        {
            "docid": 1813360,
            "score": 0.0073109501601975255
        }
    ]
    utils.assert_rest_api_hit_eq(hits_actual, hits_solution)


def test_stopwords(index_client):
    """Stopwords in query.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Query the REST API
    response = index_client.get("/api/v1/hits/?q=the+most+apache+hadoop&w=0")
    assert response.status_code == 200

    # Compare actual hits to solution hits
    hits_actual = response.get_json()["hits"]
    hits_solution = [
        {
            "docid": 6415471,
            "score": 0.21667495788863178
        },
        {
            "docid": 3133315,
            "score": 0.06738653303975232
        },
        {
            "docid": 8803912,
            "score": 0.03924084932607922
        },
        {
            "docid": 8779462,
            "score": 0.027504285343936154
        },
        {
            "docid": 28594,
            "score": 0.024636547437612663
        },
        {
            "docid": 1813360,
            "score": 0.0073109501601975255
        }
    ]
    utils.assert_rest_api_hit_eq(hits_actual, hits_solution)


def test_term_not_in_index(index_client):
    """Query term not in inverted index.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    response = index_client.get("/api/v1/hits/?q=issued+aaaaaaa&w=0.5")
    assert response.status_code == 200
    assert response.get_json() == {"hits": []}
