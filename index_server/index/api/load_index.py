import os
import index

stopwords = set()
pagerank = {}
inverted_index = {}

def load_index():
    """Load stopwords, pagerank and inverted index."""
    global stopwords, pagerank, inverted_index
    # Load stopwords
    with open(index.app.config["PATH"] + '/stopwords.txt',
            'r', encoding="utf-8") as file:
        for line in file:
            stopword = line.strip()
            stopwords.add(stopword)

    # Load PageRank values
    with open(index.app.config["PATH"] + '/pagerank.out',
            'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            doc_id, rank = line.split()
            pagerank[int(doc_id)] = float(rank)

    # Load inverted index
    index_path = index.app.config["PATH"] + '/inverted_index/' + index.app.config["INDEX_PATH"]
    with open(index_path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().split()
            term = line[0]
            idf = float(line[1])
            doc_info={}
            for i in range(2, len(line), 3):
                doc_info={
                    'doc_id':int(line[i]),
                    'term_freq': int(line[i + 1]),
                    'norm_factor': float(line[i + 2])
                    }
            inverted_index[term] = {'idf': idf, 'doc_info': doc_info}