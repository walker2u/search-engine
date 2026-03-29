import re
from collections import defaultdict
import math

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
k1 = 1.5
b = 0.75

word_to_doc_id = defaultdict(lambda: defaultdict(int))
doc_lens = {}
avg_len = 0


def tokenize(text):
    """Splits text into words, lowercase, removes punctuation."""
    return re.findall(r"\w+", text.lower())


def inverted_indexing(words, doc_id: int):
    for word in words:
        word_to_doc_id[word][doc_id] += 1


def search_word(query: str):
    words = tokenize(query)
    cand_doc_ids = set()
    for word in words:
        cand_doc_ids.update(word_to_doc_id[word].keys())
    related_docs = []
    for doc_id in cand_doc_ids:
        related_docs.append((score_doc(words, doc_id), doc_id))
    related_docs.sort(key=lambda x: x[0], reverse=True)
    return related_docs


def get_idf(word: str) -> float:
    N = len(docs)
    n = len(word_to_doc_id[word])
    return math.log(1 + (N - n + 0.5) / (n + 0.5))


def score_doc(query_words: list, doc_id: int) -> float:
    score = 0.0
    for word in query_words:
        freq = word_to_doc_id[word][doc_id]
        if freq == 0:
            continue
        doc_len = doc_lens[doc_id]
        numerator = freq * (k1 + 1)
        denominator = freq + k1 * (1 - b + b * (doc_len / avg_len))
        score += get_idf(word) * (numerator / denominator)
    return score


def main():
    global avg_len
    total = 0
    for doc_id, sentence in enumerate(docs):
        words = tokenize(sentence)
        doc_lens[doc_id] = len(words)
        inverted_indexing(words, doc_id)
        total += len(words)
    avg_len = total / len(docs)

    results = search_word("the coding")
    for score, doc_id in results:
        print(f"Score: {score:.4f} | Doc: {docs[doc_id]}")


if __name__ == "__main__":
    main()
