from engine.index import InvertedIndex
from engine.bm25 import BM25Scorer
from engine.query_parser import QueryParser
from engine.phrase import PhraseMatcher


class SearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index
        self.scorer = BM25Scorer(index)
        self.parser = QueryParser()
        self.phrase_matcher = PhraseMatcher()

    def search(self, query: str, top_k: int = 10):
        query = query.strip()

        if query.startswith('"') and query.endswith('"'):
            terms = query[1:-1].split()
            matched_docs = self.phrase_matcher.match(self.index, terms)
            scores = self.scorer.score(terms)
            scores = {d: s for d, s in scores.items() if d in matched_docs}

        else:
            terms, operator = self.parser.parse(query)
            if operator == "AND":
                scores = self._and_search(terms)
            else:
                scores = self.scorer.score(terms)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def _and_search(self, terms):
        doc_sets = []
        for term in terms:
            if term not in self.index.index:
                return {}
            doc_sets.append(set(self.index.index[term].keys()))

        common_docs = set.intersection(*doc_sets)
        scores = self.scorer.score(terms)
        return {d: s for d, s in scores.items() if d in common_docs}
