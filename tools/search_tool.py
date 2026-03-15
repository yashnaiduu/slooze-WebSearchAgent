import logging
from dataclasses import dataclass
from typing import List

from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class DuckDuckGoSearch:
    def __init__(self, max_results: int = 3):
        self._max_results = max_results

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=15),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def search(self, query: str) -> List[SearchResult]:
        from duckduckgo_search import DDGS
        from duckduckgo_search.exceptions import DuckDuckGoSearchException

        logger.info(f"DuckDuckGo search: '{query}'")
        try:
            with DDGS() as ddgs:
                raw = list(ddgs.text(query, max_results=self._max_results))
        except DuckDuckGoSearchException as exc:
            if "Ratelimit" in str(exc):
                logger.warning("DuckDuckGo rate limit hit, backing off…")
            raise

        return [
            SearchResult(
                title=r.get("title", ""),
                url=r.get("href", ""),
                snippet=r.get("body", ""),
            )
            for r in raw
        ]


class TavilySearch:
    def __init__(self, max_results: int = 5):
        self._max_results = max_results

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), reraise=True)
    def search(self, query: str) -> List[SearchResult]:
        import httpx

        logger.info(f"Tavily search: '{query}'")
        response = httpx.post(
            "https://api.tavily.com/search",
            json={
                "api_key": settings.TAVILY_API_KEY,
                "query": query,
                "max_results": self._max_results,
            },
            timeout=settings.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        return [
            SearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                snippet=r.get("content", ""),
            )
            for r in data.get("results", [])
        ]


class SerpAPISearch:
    def __init__(self, max_results: int = 5):
        self._max_results = max_results

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), reraise=True)
    def search(self, query: str) -> List[SearchResult]:
        import httpx

        logger.info(f"SerpAPI search: '{query}'")
        response = httpx.get(
            "https://serpapi.com/search",
            params={
                "api_key": settings.SERPAPI_API_KEY,
                "q": query,
                "num": self._max_results,
            },
            timeout=settings.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        return [
            SearchResult(
                title=r.get("title", ""),
                url=r.get("link", ""),
                snippet=r.get("snippet", ""),
            )
            for r in data.get("organic_results", [])[:self._max_results]
        ]


_SEARCH_PROVIDERS = {
    "duckduckgo": DuckDuckGoSearch,
    "tavily": TavilySearch,
    "serpapi": SerpAPISearch,
}


def get_search_tool(max_results: int | None = None):
    provider = settings.SEARCH_PROVIDER.lower()
    cls = _SEARCH_PROVIDERS.get(provider)
    if cls is None:
        raise ValueError(f"Unsupported search provider '{provider}'. Supported: {list(_SEARCH_PROVIDERS.keys())}")
    return cls(max_results=max_results or settings.MAX_SEARCH_RESULTS)
