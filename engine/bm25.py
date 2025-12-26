import math
from engine.index import InvertedIndex


class BM25Scorer:
    def __init__(self, index: InvertedIndex, k1: float = 1.5, b: float = 0.75):
        self.index = index
        self.k1 = k1
        self.b = b

    def avg_doc_length(self) -> float:
        total_length = sum(self.index.doc_lengths.values())
        return total_length / self.index.document_count

    def idf(self, term: str) -> float:
        df = len(self.index.index.get(term, {}))
        if df == 0:
            return 0.0
        return math.log((self.index.document_count - df + 0.5) / (df + 0.5) + 1)

    def score(self, query_terms: list[str]) -> dict[int, float]:
        scores = {}
        avg_dl = self.avg_doc_length()

        for term in query_terms:
            if term not in self.index.index:
                continue

            idf_value = self.idf(term)
            postings = self.index.index[term]

            for doc_id, positions in postings.items():
                tf = len(positions)
                dl = self.index.doc_lengths[doc_id]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (dl / avg_dl))
                score = idf_value * (numerator / denominator)
            scores[doc_id] = scores.get(doc_id, 0.0) + score

        return scores
