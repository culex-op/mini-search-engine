from collections import defaultdict
from engine.tokenizer import tokenize
import json

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)
        self.document_count = 0
        self.doc_lengths = {}
        
    def add_document(self, doc_id: int, text: str):
        tokens = tokenize(text)
        term_frequencies = {}
        self.doc_lengths[doc_id] = len(tokens)

        for token in tokens:
            term_frequencies[token] = term_frequencies.get(token, 0) + 1

        for term, freq in term_frequencies.items():
            self.index[term][doc_id] = freq

        self.document_count += 1
    def save(self, filepath: str):
        data = {
            "index": self.index,
            "doc_lengths": self.doc_lengths,
            "document_count": self.document_count
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load(self, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)

        self.index = {term: {int(doc): freq for doc, freq in docs.items()}
                      for term, docs in data["index"].items()}
        self.doc_lengths = {int(doc): length for doc, length in data["doc_lengths"].items()}
        self.document_count = data["document_count"]