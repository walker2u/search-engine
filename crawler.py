from collections import deque
from bs4 import BeautifulSoup
import requests
from indexer import add_document
from urllib.parse import urljoin


def crawl(seed_url: str, max_pages):
    queue = deque()
    visited = set()
    pages_indexed = 0

    queue.append(seed_url)
    visited.add(seed_url)

    while len(queue) != 0 and pages_indexed < max_pages:
        url = queue.popleft()
        print(f"[{pages_indexed + 1}/{max_pages}] Crawling: {url}")

        try:
            headers = {"User-Agent": "MyPythonSearchEngineBot/1.0"}
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code != 200:
                print(f"  -> Skipped: Got status code {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

            add_document(url, text)
            pages_indexed += 1

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if full_url.startswith("https") and full_url not in visited:
                    visited.add(full_url)
                    queue.append(full_url)

        except Exception as e:
            print(f"  -> Error crawling {url}: {e}")
            continue


if __name__ == "__main__":
    from indexer import init_db

    print("Initializing Db-")
    init_db()
    print("Starting Crawler-")
    crawl("https://en.wikipedia.org/wiki/Search_engine", 20)
    print("Crawling Complete!")
