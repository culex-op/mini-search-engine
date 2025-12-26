class PhraseMatcher:
    def match(self, index, terms: list[str]) -> set[int]:
        if not terms:
            return set()

        postings = index.index.get(terms[0], {})
        candidate_docs = set(postings.keys())

        for term in terms[1:]:
            candidate_docs &= set(index.index.get(term, {}).keys())

        results = set()

        for doc_id in candidate_docs:
            positions = index.index[terms[0]][doc_id]

            for pos in positions:
                match = True
                for offset, term in enumerate(terms[1:], start=1):
                    if (pos + offset) not in index.index[term][doc_id]:
                        match = False
                        break
                if match:
                    results.add(doc_id)
                    break

        return results
