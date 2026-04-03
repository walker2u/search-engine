from sentence_transformers import SentenceTransformer
import sqlite3
import math
import re
from collections import defaultdict
import numpy as np


class HybridSearchEngine:
    def __init__(self, db_path="search.db"):
        # model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # DB
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT COUNT(id) from documents")
        self.total_docs = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT AVG(doc_length) from documents")
        self.avg_doc_len = self.cursor.fetchone()[0]

        if self.avg_doc_len is None:
            self.avg_doc_len = 1

        self.k1 = 1.5
        self.b = 0.75

    def tokenize(self, query: str):
        return re.findall(r"\w+", query.lower())

    def get_idf(self, freq):
        return math.log(1 + (self.total_docs - freq + 0.5) / (freq + 0.5))

    def bm25_search(self, query: str):
        words = self.tokenize(query)
        document_scores = defaultdict(float)

        for word in words:

            self.cursor.execute("SELECT id FROM terms WHERE word=?", (word,))
            term_res = self.cursor.fetchone()
            if not term_res:
                continue
            term_id = term_res[0]

            self.cursor.execute(
                "SELECT COUNT(doc_id) FROM postings WHERE term_id = ?", (term_id,)
            )
            doc_freq = self.cursor.fetchone()[0]
            idf = self.get_idf(doc_freq)

            self.cursor.execute(
                "SELECT p.doc_id,p.frequency,d.doc_length FROM postings as p INNER JOIN documents as d ON p.doc_id = d.id WHERE term_id = ?",
                (term_id,),
            )
            docid_freq_doc_len = self.cursor.fetchall()

            for doc_id, freq, doc_len in docid_freq_doc_len:
                if freq == 0:
                    continue

                numerator = freq * (self.k1 + 1)
                denominator = freq + self.k1 * (
                    1 - self.b + self.b * (doc_len / self.avg_doc_len)
                )
                document_scores[doc_id] += idf * (numerator / denominator)
        return sorted(document_scores.items(), key=lambda o: o[1], reverse=True)

    def vector_search(self, query: str):
        query_vector = self.model.encode(query)

        self.cursor.execute("SELECT id, url, embedding FROM documents")
        docs = self.cursor.fetchall()

        document_scores = defaultdict(float)
        for doc_id, url, embedding in docs:
            doc_vector = np.frombuffer(embedding, dtype=np.float32)
            score = np.dot(doc_vector, query_vector)
            document_scores[doc_id] = score

        return sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

    def hybrid_search(self, query: str, k=60):
        bm25_score = self.bm25_search(query)
        vector_score = self.vector_search(query)

        rrf_scores = defaultdict(float)

        for rank, (doc_id, score) in enumerate(bm25_score, start=1):
            rrf_scores[doc_id] = 1.0 / (k + rank)
        for rank, (doc_id, score) in enumerate(vector_score, start=1):
            rrf_scores[doc_id] += 1.0 / (k + rank)

        return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":

    print("Starting Search Engine...")
    engine = HybridSearchEngine("../search.db")

    print("\n Running Search Engine...")
    related_docs = engine.hybrid_search("search engine")

    for doc_id, score in related_docs:
        engine.cursor.execute("SELECT url FROM documents WHERE id = ?", (doc_id,))
        url = engine.cursor.fetchone()[0]
        print(f"Score: {score:.4f} | URL: {url}")
