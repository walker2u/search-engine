import re
from collections import defaultdict

docs = [
    "The quick brown fox jumps over the lazy dog",
    "Apple pie is delicious with vanilla ice cream",
    "Learning data structures improves coding skills",
    "The secret to success is consistent practice",
    "Pie charts are useful for visualizing proportions",
    "Memory management matters in system design",
    "Open source contributions grow community knowledge",
    "Never stop exploring new algorithms and techniques",
    "Coding every day builds strong problem-solving habits",
    "Banana smoothies taste great on summer mornings",
]

wordToDoc = defaultdict(set)


def tokenize_and_index(docs: list):
    for doc_id, text in enumerate(docs):
        words = re.findall(r"\w+", text.lower())
        for word in words:
            if word in wordToDoc:
                (id, cnt) = wordToDoc[word]
                wordToDoc[word] = {id, cnt + 1}
            else:
                wordToDoc[word].add((doc_id, 0))


def search(query: str):
    query_words = re.findall(r"\w+", query.lower())

    if not query_words:
        return []

    first_word = query_words[0]
    result_ids = wordToDoc.get(first_word, set()).copy()

    current_op = "OR"

    i = 1
    while i < len(query_words):
        token = query_words[i]

        if token in ("and", "or", "not"):
            current_op = token.upper()
        else:
            next_docs = wordToDoc.get(token, set())

            if current_op == "AND":
                result_ids &= next_docs
            elif current_op == "OR":
                result_ids |= next_docs
            elif current_op == "NOT":
                result_ids -= next_docs

            current_op = "OR"

        i += 1

    return [docs[id] for id in result_ids]


def main():
    tokenize_and_index(docs)

    print("--- Search: 'the knowledge day' ---")
    results = search("the knowledge day")
    for r in results:
        print(f"- {r}")

    print("\n--- Search: 'the AND dog' ---")
    results = search("the and dog")
    for r in results:
        print(f"- {r}")

    print("\n--- Search: 'pie NOT apple' ---")
    results = search("pie not apple")
    for r in results:
        print(f"- {r}")


if __name__ == "__main__":
    main()
