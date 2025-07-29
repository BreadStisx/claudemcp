"""Simple web search plugin using DuckDuckGo HTML."""
import requests
from urllib.parse import quote_plus
from html.parser import HTMLParser


class _ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._in_result = False
        self._current = {}
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._tag_stack.append(tag)
        if tag == "a" and "result__a" in attrs_dict.get("class", ""):
            self._in_result = True
            self._current = {"url": attrs_dict.get("href", ""), "title": ""}

    def handle_endtag(self, tag):
        if self._tag_stack:
            self._tag_stack.pop()
        if tag == "a" and self._in_result:
            self._in_result = False
            if self._current.get("title"):
                self.results.append(self._current)

    def handle_data(self, data):
        if self._in_result:
            self._current["title"] += data.strip()


def search(query: str, max_results: int = 5) -> list[dict]:
    """Search DuckDuckGo and return results."""
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; claudemcp/0.1)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        parser = _ResultParser()
        parser.feed(resp.text)
        return parser.results[:max_results]
    except Exception as exc:
        return [{"error": str(exc)}]


def fetch_page(url: str, max_length: int = 5000) -> str:
    """Fetch a URL and return text content."""
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; claudemcp/0.1)"
        })
        resp.raise_for_status()
        text = resp.text[:max_length]
        return text
    except Exception as exc:
        return f"error fetching {url}: {exc}"


