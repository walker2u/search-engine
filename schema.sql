CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    content TEXT,
    doc_length INTEGER
);

CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY,
    word TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS postings (
    term_id INTEGER REFERENCES terms(id),
    doc_id INTEGER REFERENCES documents(id),
    frequency INTEGER,
    PRIMARY KEY (term_id, doc_id)
);