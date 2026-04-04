import sys
import os
from fastapi import FastAPI
import re
from fastapi.middleware.cors import CORSMiddleware

current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the /api folder
project_root = os.path.dirname(current_dir)  # Gets the parent folder

# 2. Tell Python to look in the project root for imports
sys.path.append(project_root)

from oops.engine import HybridSearchEngine

app = FastAPI()
engine = HybridSearchEngine("../search.db")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,  # Allows cookies/auth headers
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/search")
def api_search(query: str):
    results = engine.hybrid_search(query)

    query_words = re.findall(r"\w+", query.lower())
    first_word = query_words[0] if query_words else ""

    escaped_words = [re.escape(w) for w in query_words]
    pattern = re.compile(r"\b(" + "|".join(escaped_words) + r")\b", re.IGNORECASE)

    formatted_results = []
    for rank, (doc_id, score) in enumerate(results[:10], start=1):
        engine.cursor.execute(
            "SELECT url, SUBSTR(content,MAX(1, INSTR(LOWER(content),?)-60),150) FROM documents WHERE id = ?",
            (
                first_word,
                doc_id,
            ),
        )
        row = engine.cursor.fetchone()
        if not row:
            continue
        url = row[0]
        raw_content = row[1]

        highlighted_content = pattern.sub(r"<b>\1</b>", raw_content)

        formatted_results.append(
            {
                "rank": rank,
                "url": url,
                "content": f"...{highlighted_content}...",
                "score": round(score, 4),
            }
        )
    return {"query": query, "results": formatted_results}
