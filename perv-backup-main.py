import math
import re
from collections import defaultdict

# --- CONFIGURATION ---
k1 = 1.5  # Controls how much term frequency matters
b = 0.75  # Controls how much document length matters

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

# 1. The Index: word -> {doc_id -> frequency}
index = defaultdict(lambda: defaultdict(int))

# 2. Metadata for BM25
doc_lengths = {}  # {doc_id -> number of words}
avg_doc_length = 0
total_docs = len(docs)


def tokenize(text):
    """Splits text into words, lowercase, removes punctuation."""
    return re.findall(r"\w+", text.lower())


def build_index():
    global avg_doc_length
    total_word_count = 0

    for doc_id, text in enumerate(docs):
        words = tokenize(text)

        # Save document length
        doc_lengths[doc_id] = len(words)
        total_word_count += len(words)

        # Build Index (Count frequency)
        for word in words:
            index[word][doc_id] += 1

    # Calculate Average Document Length
    avg_doc_length = total_word_count / total_docs


def calculate_idf(term):
    """
    Inverse Document Frequency:
    High value if word is rare (e.g., 'quantum').
    Low value if word is common (e.g., 'the').
    """
    # How many docs contain this term?
    doc_count_containing_term = len(index[term])

    if doc_count_containing_term == 0:
        return 0

    # Standard IDF formula
    return math.log(
        1
        + (total_docs - doc_count_containing_term + 0.5)
        / (doc_count_containing_term + 0.5)
    )


def score_doc(query_terms, doc_id):
    """
    Calculates the BM25 score for a specific document against a query.
    """
    score = 0

    for term in query_terms:
        if term not in index:
            continue

        # 1. Get Term Frequency (How often term appears in this doc)
        freq = index[term][doc_id]
        if freq == 0:
            continue

        # 2. Get IDF (How rare is this term globally?)
        idf = calculate_idf(term)

        # 3. Document Length Normalization
        # Long docs are penalized slightly so they don't win just by being long
        doc_len = doc_lengths[doc_id]

        # The BM25 Formula
        numerator = freq * (k1 + 1)
        denominator = freq + k1 * (1 - b + b * (doc_len / avg_doc_length))

        score += idf * (numerator / denominator)

    return score


def search(query):
    query_terms = tokenize(query)

    # 1. Find potential documents (Docs that contain at least one query word)
    candidate_docs = set()
    for term in query_terms:
        candidate_docs.update(index[term].keys())

    if not candidate_docs:
        return []

    # 2. Score every candidate document
    scored_results = []
    for doc_id in candidate_docs:
        score = score_doc(query_terms, doc_id)
        scored_results.append((score, docs[doc_id]))

    # 3. Sort by score (Highest first)
    scored_results.sort(key=lambda x: x[0], reverse=True)

    return scored_results


def main():
    build_index()

    # Example 1: "The" is common (low score), "Fox" is rare (high score)
    print("--- Search: 'the fox' ---")
    results = search("the fox")
    for score, text in results:
        print(f"[{score:.4f}] {text}")

    # Example 2: Compare lengths
    print("\n--- Search: 'coding' ---")
    results = search("coding")
    for score, text in results:
        print(f"[{score:.4f}] {text}")


if __name__ == "__main__":
    main()
