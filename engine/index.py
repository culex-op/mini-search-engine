from collections import defaultdict
from pydoc import text
from engine.tokenizer import tokenize
import json

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)
        self.document_count = 0
        self.doc_lengths = {}
        self.documents = {}
    
    def add_document(self, doc_id: int, text: str):
        self.documents[doc_id] = text

        tokens = tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        for position, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = defaultdict(list)
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = []

            self.index[token][doc_id].append(position)

        self.document_count += 1

    def save(self, filepath: str):
        data = {
            "index": self.index,
            "doc_lengths": self.doc_lengths,
            "document_count": self.document_count,
            "documents": self.documents
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load(self, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)
        self.index = defaultdict(lambda: defaultdict(list))
        for term, docs in data["index"].items():
            for doc_id, positions in docs.items():
                self.index[term][int(doc_id)] = positions

        self.doc_lengths = {int(doc): length for doc, length in data["doc_lengths"].items()}
        self.documents = {int(doc): text for doc, text in data["documents"].items()}
        self.document_count = data["document_count"]
