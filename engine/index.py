from collections import defaultdict
from engine.tokenizer import tokenize


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)
        self.document_count = 0

    def add_document(self, doc_id: int, text: str):
        tokens = tokenize(text)
        term_frequencies = {}

        for token in tokens:
            term_frequencies[token] = term_frequencies.get(token, 0) + 1

        for term, freq in term_frequencies.items():
            self.index[term][doc_id] = freq

        self.document_count += 1
