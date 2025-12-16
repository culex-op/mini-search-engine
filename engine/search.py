from engine.tokenizer import tokenize
from engine.index import InvertedIndex


class SearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def search(self, query: str) -> set[int]:
        tokens = tokenize(query)
        results = set()

        for token in tokens:
            if token in self.index.index:
                results.update(self.index.index[token].keys())

        return results
