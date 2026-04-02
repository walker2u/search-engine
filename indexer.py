import sqlite3
from main import tokenize
from collections import defaultdict
from sentence_transformers import SentenceTransformer
import numpy as np

sql_file_name = "schema.sql"
model = SentenceTransformer("all-MiniLM-L6-v2")


def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    with open(sql_file_name, "r") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()


def get_conn():
    return sqlite3.connect("search.db")


def add_document(url: str, text: str):
    words_list = tokenize(text)
    word_counts = defaultdict(int)
    for word in words_list:
        word_counts[word] += 1

    # converting text into vector then saving it
    vector = model.encode(text)
    vec_bytes = vector.tobytes()

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (url,content,doc_length,embedding) VALUES(?,?,?,?)",
        (url, text, len(words_list), vec_bytes),
    )
    doc_id = cursor.lastrowid

    for word, freq in word_counts.items():
        cursor.execute("INSERT OR IGNORE INTO terms (word) VALUES (?)", (word,))
        cursor.execute("SELECT id FROM terms where word=?", (word,))
        term_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO postings (term_id,doc_id,frequency) VALUES(?,?,?)",
            (term_id, doc_id, freq),
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # init_db()
    add_document(
        "https://en.wikipedia.org/wiki/Apple",
        "Apple is a fruit. A delicious red apple.",
    )
    add_document(
        "https://en.wikipedia.org/wiki/Banana",
        "Banana is yellow. I like banana and apple.",
    )
    print("Documents indexed successfully!")
