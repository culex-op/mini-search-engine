import math
from engine.index import InvertedIndex


class TFIDFScorer:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def idf(self, term: str) -> float:
        df = len(self.index.index.get(term, {}))
        if df == 0:
            return 0.0
        return math.log(self.index.document_count / df)

    def score(self, query_terms: list[str]) -> dict[int, float]:
        scores = {}

        for term in query_terms:
            if term not in self.index.index:
                continue

            idf_value = self.idf(term)
            postings = self.index.index[term]

            for doc_id, tf in postings.items():
                scores[doc_id] = scores.get(doc_id, 0.0) + tf * idf_value

        return scores
