import json

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
