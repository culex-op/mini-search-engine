from engine.tokenizer import tokenize
from engine.index import InvertedIndex
from engine.bm25 import BM25Scorer


class SearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index
        self.scorer = BM25Scorer(index)

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        query_terms = tokenize(query)
        scores = self.scorer.score(query_terms)

        ranked_results = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked_results[:top_k]
