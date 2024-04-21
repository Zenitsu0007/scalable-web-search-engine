"""
Search server index views
"""
import threading
import heapq
import requests
import flask
from flask import request, render_template
import search.model

class Search:
    def __init__(self, index_urls, query, weight):
        self.index_urls = index_urls
        self.query = query
        self.weight = weight
        self.hits = []
        self.threads = []

    def fetch_hits(self, url):
        """Fetch hits from an index server."""
        try:
            params = {'q': self.query, 'w': self.weight}
            response = requests.get(url, params=params, timeout=1)
            if response.status_code == 200:
                for hit in response.json()['hits']:
                    heapq.heappush(self.hits, 
                                   (-hit['score'], hit['docid'], hit))
        except requests.RequestException as e:
            print(f"Error contacting {url}: {e}")

    def start_search(self):
        """Start threads to fetch hits from all index servers."""
        for url in self.index_urls:
            thread = threading.Thread(target=self.fetch_hits, args=(url,))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def get_top_hits(self, num_results=10):
        """Retrieve the top N hits based on score."""
        return [heapq.heappop(self.hits)[-1] for _ in 
                range(min(len(self.hits), num_results))]

@search.app.route('/', methods=['GET'])
def show_index():
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)
    if not query:
        context = {"docs": [], "query": "", "weight": 0.5}
        return flask.render_template('index.html', **context)
    if not weight:
        weight = 0.5

    index_urls = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']
    search_instance = Search(index_urls, query, weight)
    search_instance.start_search()
    top_hits = search_instance.get_top_hits()

    # Fetch document details from the database
    db = search.model.get_db()
    docs = []
    for hit in top_hits:
        doc = db.execute(
            'SELECT * '
            'FROM Documents '
            'WHERE docid == ? ', 
            (hit['docid'],)).fetchone()
        if doc and not doc['summary']:
            doc['summary'] = 'No summary available'
        docs.append(doc)

    context = {"docs": docs, "query": query, "weight": weight}

    return render_template('index.html', **context)