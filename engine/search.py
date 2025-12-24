from engine.tokenizer import tokenize
from engine.index import InvertedIndex
from engine.bm25 import BM25Scorer
from engine.query_parser import QueryParser


class SearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index
        self.scorer = BM25Scorer(index)
        self.parser = QueryParser()

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        terms, operator = self.parser.parse(query)

        if operator == "OR":
            scores = self.scorer.score(terms)

        else:  # AND
            scores = self._and_search(terms)

        ranked_results = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked_results[:top_k]

    def _and_search(self, terms: list[str]) -> dict[int, float]:
        doc_sets = []

        for term in terms:
            if term not in self.index.index:
                return {}
            doc_sets.append(set(self.index.index[term].keys()))

        common_docs = set.intersection(*doc_sets)
        scores = self.scorer.score(terms)

        return {doc: score for doc, score in scores.items() if doc in common_docs}
