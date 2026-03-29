from collections import deque
import requests
import BeautifulSoup


def crawl(seed_url: str, max_pages):
    queue = deque()
    visited = set()
    queue.insert(seed_url)
    while len(queue) != 0 and len(visited) < max_pages:
        url = queue.pop()
        if url in visited:
            continue
        visited.add(url)
        try:
            response = requests.get(url, timeout=3)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
        except:
            continue
