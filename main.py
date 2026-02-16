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

wordToDoc = defaultdict(lambda: defaultdict(int))


def tokenize_and_index(docs: list):
    for doc_id, text in enumerate(docs):
        words = re.findall(r"\w+", text.lower())
        for word in words:
            wordToDoc[word][doc_id] += 1


def search(query: str):
    query_words = re.findall(r"\w+", query.lower())

    if not query_words:
        return []

    first_word = query_words[0]
    if first_word in wordToDoc:
        result_ids = set(wordToDoc.get(first_word))
    else:
        result_ids = set()

    current_op = "OR"

    i = 1
    while i < len(query_words):
        token = query_words[i]

        if token in ("and", "or", "not"):
            current_op = token.upper()
        else:
            if token in wordToDoc:
                docs_for_word = set(wordToDoc.get(token))
            else:
                docs_for_word = set()

            if result_ids is None:
                result_ids = docs_for_word.copy()
            elif current_op == "AND":
                result_ids &= docs_for_word
            elif current_op == "OR":
                result_ids |= docs_for_word
            elif current_op == "NOT":
                result_ids -= docs_for_word

            current_op = "OR"

        i += 1

    sorted_res = list()
    print(result_ids)
    for r in result_ids:
        sorted_res.append(docs[r])
    return sorted_res


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
