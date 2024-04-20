"""Public Search Server tests."""

import subprocess
import re
import threading
import bs4


def test_concurrency(search_client, mocker):
    """Verify search is efficient through concurrent requests.

    'search_client' is a fixture function that provides a Flask test server
    interface

    Note: 'mocker' is a fixture function provided by the pytest-mock package.
    This fixture lets us override a library function with a temporary fake
    function that returns a hardcoded value while testing.

    Fixtures are implemented in conftest.py and reused by many tests.  Docs:
    https://docs.pytest.org/en/latest/fixture.html
    """
    spy = mocker.spy(threading.Thread, "start")
    response = search_client.get("/?q=hello+world")
    assert response.status_code == 200
    assert spy.call_count == 3


def test_inputs(search_client):
    """Verify the search page has the required form inputs.

    'search_client' is a fixture function that provides a Flask test server
    interface

    Fixtures are implemented in conftest.py and reused by many tests.  Docs:
    https://docs.pytest.org/en/latest/fixture.html
    """
    # Load search server main page
    response = search_client.get("/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")

    # Inputs for "q" and "w"
    form_input_names = [
        submit.get("name") for button in soup.find_all('form')
        for submit in button.find_all("input") if submit
    ]
    assert "q" in form_input_names
    assert "w" in form_input_names

    # Inputs types
    form_input_types = [
        submit.get("type") for button in soup.find_all('form')
        for submit in button.find_all("input") if submit
    ]
    assert "text" in form_input_types
    assert "range" in form_input_types
    assert "submit" in form_input_types


def test_simple(search_client):
    """Verify a search returns any results at all.

    'search_client' is a fixture function that provides a Flask test server
    interface

    Fixtures are implemented in conftest.py and reused by many tests.  Docs:
    https://docs.pytest.org/en/latest/fixture.html
    """
    # Load search server main page after search
    response = search_client.get("/?q=hello+world")
    soup = response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")

    # Verify query is displayed.
    query = soup.find(type="text")["value"]
    assert query == "hello world"

    # Make sure some doc titles show up
    assert soup.find_all("div", {"class": "doc_title"})


def test_titles(search_client):
    """Verify doc titles in results for a query with one term.

    'search_client' is a fixture function that provides a Flask test server
    interface

    Fixtures are implemented in conftest.py and reused by many tests.  Docs:
    https://docs.pytest.org/en/latest/fixture.html
    """
    # Load search server page with search query
    response = search_client.get("/?q=mapreduce&w=0.22")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")

    # Verify query and weight are displayed
    query = soup.find(type="text")["value"]
    assert query == "mapreduce"
    weight = soup.find(type="range")["value"]
    assert weight == "0.22"

    # Verify resulting document titles
    doc_titles = soup.find_all("div", {"class": "doc_title"})
    assert len(doc_titles) == 10

    doc_titles_text = [re.sub(r"\s+", " ", x.text.strip()) for x in doc_titles]
    assert doc_titles_text == [
        "MapReduce",
        "Native cloud application",
        "Big data",
        "Google File System",
        "Distributed file system for cloud",
        "Stream processing",
        "Divide-and-conquer algorithm",
        "ChromiumOS",
        "List of computer scientists",
        "Computer cluster"
    ]


def test_summaries_urls(search_client):
    """Verify summaries and URLs in results for a query with one term.

    'search_client' is a fixture function that provides a Flask test server
    interface

    Fixtures are implemented in conftest.py and reused by many tests.  Docs:
    https://docs.pytest.org/en/latest/fixture.html
    """
    # Load search server page with search query
    response = search_client.get("/?q=nlp&w=0")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")

    # Verify query and weight are displayed
    query = soup.find(type="text")["value"]
    assert query == "nlp"
    weight = soup.find(type="range")["value"]
    assert float(weight) == 0.0

    # Verify resulting document titles
    doc_titles = soup.find_all("div", {"class": "doc_title"})
    assert len(doc_titles) == 10

    doc_titles_text = [re.sub(r"\s+", " ", x.text.strip()) for x in doc_titles]
    assert doc_titles_text == [
        "NLP",
        "Natural language processing",
        "Process engineering",
        "List of important publications in computer science",
        "Artificial intelligence",
        "List of computer science awards",
        "Scientific modelling",
        "Automated decision-making",
        "Linear programming",
        "Unsupervised learning"
        ]

    doc_summaries = soup.find_all("div", {"class": "doc_summary"})
    assert len(doc_summaries) == 10

    doc_summary_text = [re.sub(r"\s+", " ", x.text.strip())
                        for x in doc_summaries]
    assert doc_summary_text == [
        "No summary available",
        "Natural language processing (NLP) is an interdisciplinary "
        "subfield of computer science and linguistics. It is primarily "
        "concerned with giving computers the ability to support and "
        "manipulate speech. It involves processing natural language "
        "datasets,...",
        "Process engineering is the understanding and application of the "
        "fundamental principles and laws of nature that allow humans to "
        "transform raw material and energy into products that are useful "
        "to society, at an industrial level.[1] By taking advanta...",
        "This is a list of important publications in computer science, "
        "organized by field. Some reasons why a particular publication "
        "might be regarded as important:...",
        "Artificial intelligence (AI) is the intelligence of machines or "
        "software, as opposed to the intelligence of humans or animals. It "
        "is also the field of study in computer science that develops and "
        'studies intelligent machines. "AI" may also refer to...',
        "This list of computer science awards is an index to articles "
        "on notable awards related to computer science. It includes "
        "lists of awards by the Association for Computing Machinery, the "
        "Institute of Electrical and Electronics Engineers, other comput...",
        "Scientific modelling is an activity that produces models "
        "representing empirical objects, phenomena, and physical processes, "
        "to make a particular part or feature of the world easier to "
        "understand, define, quantify, visualize, or simulate. It requir...",
        "Automated decision-making (ADM) involves the use of data, machines "
        "and algorithms to make decisions in a range of contexts, including "
        "public administration, business, health, education, law, employment, "
        "transport, media and entertainment, with var...",
        "Linear programming (LP), also called linear optimization, is a "
        "method to achieve the best outcome (such as maximum profit or "
        "lowest cost) in a mathematical model whose requirements are "
        "represented by linear relationships. Linear programming is a s...",
        "Unsupervised learning is a paradigm in machine learning where, in "
        "contrast to supervised learning and semi-supervised learning, "
        "algorithms learn patterns exclusively from unlabeled data....",
    ]

    doc_urls = soup.find_all("a", {"class": "doc_url"})
    assert len(doc_urls) == 10

    doc_url_text = [re.sub(r"\s+", " ", x.text.strip())
                    for x in doc_urls]
    assert doc_url_text == [
        "https://en.wikipedia.org/wiki/NLP",
        "https://en.wikipedia.org/wiki/Natural_language_processing",
        "https://en.wikipedia.org/wiki/Process_engineering",
        "https://en.wikipedia.org/wiki/"
        "List_of_important_publications_in_computer_science",
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/List_of_computer_science_awards",
        "https://en.wikipedia.org/wiki/Scientific_modelling",
        "https://en.wikipedia.org/wiki/Automated_decision-making",
        "https://en.wikipedia.org/wiki/Linear_programming",
        "https://en.wikipedia.org/wiki/Unsupervised_learning",
    ]


def test_html(search_client, tmpdir):
    """Verify HTML5 compliance in HTML portion of the search pages.

    'search_client' is a fixture function that provides a Flask test server
    interface

    Fixtures are implemented in conftest.py and reused by many tests.  Docs:
    https://docs.pytest.org/en/latest/fixture.html

    'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture
    """
    # Validate HTML of search page before a search
    download(search_client, "/", tmpdir/"index.html")
    subprocess.run(
        [
            "html5validator", "--ignore=JAVA_TOOL_OPTIONS",
            str(tmpdir/"index.html"),
        ],
        check=True,
    )

    # Validate HTML of search page after a search with no results
    download(search_client, "/?q=&w=0.01", tmpdir/"blank_query.html")
    subprocess.run(
        [
            "html5validator", "--ignore=JAVA_TOOL_OPTIONS",
            str(tmpdir/"blank_query.html"),
        ],
        check=True,
    )

    # Validate HTML of search page after a successful search
    download(search_client, "/?q=dogs&w=0.22", tmpdir/"simple_query.html")
    subprocess.run(
        [
            "html5validator", "--ignore=JAVA_TOOL_OPTIONS",
            str(tmpdir/"simple_query.html"),
        ],
        check=True,
    )


def download(search_client, url, outpath):
    """Load url using driver and save to outputpath."""
    response = search_client.get(url)
    assert response.status_code == 200

    soup = bs4.BeautifulSoup(response.data, "html.parser")
    html = soup.prettify()

    # Write HTML of current page source to file
    outpath.write_text(html, encoding='utf-8')
