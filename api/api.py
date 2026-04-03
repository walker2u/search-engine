import sys
import os
from fastapi import FastAPI

current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the /api folder
project_root = os.path.dirname(current_dir)  # Gets the parent folder

# 2. Tell Python to look in the project root for imports
sys.path.append(project_root)

from oops.engine import HybridSearchEngine

app = FastAPI()
engine = HybridSearchEngine("../search.db")


@app.get("/search")
def api_search(query: str):
    results = engine.hybrid_search(query)

    formatted_results = []
    for rank, (doc_id, score) in enumerate(results, start=1):
        engine.cursor.execute("SELECT url FROM documents WHERE id = ?", (doc_id,))
        url = engine.cursor.fetchone()[0]

        formatted_results.append({"rank": rank, "url": url, "score": score})
    return {"query": query, "results": formatted_results}
