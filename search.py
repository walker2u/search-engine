import re
from indexer import get_conn
from collections import defaultdict
import math


k1 = 1.5
b = 0.75

conn = get_conn()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(id) FROM documents")
total_docs = cursor.fetchone()[0]
cursor.execute("SELECT AVG(doc_length) FROM documents")
avg_docs_length = cursor.fetchone()[0]


def tokenize(text):
    """Splits text into words, lowercase, removes punctuation."""
    return re.findall(r"\w+", text.lower())


def get_idf(doc_freq) -> float:
    return math.log(1 + (total_docs - doc_freq + 0.5) / (doc_freq + 0.5))


def search(query: str):

    words = tokenize(query)
    document_scores = defaultdict(float)
    for word in words:
        cursor.execute("SELECT id FROM terms WHERE word=?", (word,))
        term_res = cursor.fetchone()
        if not term_res:
            continue
        term_id = term_res[0]
        cursor.execute("SELECT COUNT(doc_id) FROM postings WHERE term_id=?", (term_id,))
        doc_freq = cursor.fetchone()[0]
        idf = get_idf(doc_freq)

        cursor.execute(
            "SELECT post.doc_id,post.frequency,doc.doc_length FROM postings as post INNER JOIN documents as doc on post.doc_id = doc.id where term_id=?",
            (term_id,),
        )
        doc_id_freq_doc_len = cursor.fetchall()
        for doc_id, freq, doc_len in doc_id_freq_doc_len:
            if freq == 0:
                continue
            numerator = freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * (doc_len / avg_docs_length))
            document_scores[doc_id] += idf * (numerator / denominator)
    return sorted(document_scores.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    document_scores = search("search engine")
    for doc_id, score in document_scores:
        cursor.execute("SELECT url FROM documents WHERE id=?", (doc_id,))
        url = cursor.fetchone()[0]
        print(f"url : {url}, score : {score}")
