from engine.index import InvertedIndex
from engine.search import SearchEngine


def main():
    index = InvertedIndex()

    index.add_document(1, "Search engines are fascinating systems")
    index.add_document(2, "Building a search engine from scratch is educational")
    index.add_document(3, "This project demonstrates how search works internally")

    search_engine = SearchEngine(index)

    queries = [
        "search engine",
        "project",
        "systems",
        "python"
    ]

    for query in queries:
        results = search_engine.search(query)
        print(f"Query: '{query}' -> Results: {results}")


if __name__ == "__main__":
    main()
