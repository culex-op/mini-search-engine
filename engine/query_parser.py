from engine.tokenizer import tokenize


class QueryParser:
    def parse(self, query: str) -> tuple[list[str], str]:
        """
        Returns (terms, operator)
        operator ∈ {"OR", "AND"}
        """

        tokens = tokenize(query)

        if "and" in tokens:
            terms = [t for t in tokens if t != "and"]
            return terms, "AND"

        if "or" in tokens:
            terms = [t for t in tokens if t != "or"]
            return terms, "OR"

        return tokens, "OR"
