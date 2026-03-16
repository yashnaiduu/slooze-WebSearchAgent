import logging
import httpx
import time
from dataclasses import dataclass
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

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

    def search(self, query: str) -> List[SearchResult]:
        logger.info(f"DuckDuckGo search: '{query}'")

        delays = [5, 15, 30, 60]
        for attempt, delay in enumerate(delays, 1):
            try:
                with DDGS() as ddgs:
                    raw = list(ddgs.text(query, max_results=self._max_results))
                return [
                    SearchResult(
                        title=r.get("title", ""),
                        url=r.get("href", ""),
                        snippet=r.get("body", ""),
                    )
                    for r in raw
                ]
            except DuckDuckGoSearchException as exc:
                if "Ratelimit" in str(exc):
                    logger.warning(f"DuckDuckGo rate limit (attempt {attempt}), retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    logger.error(f"DuckDuckGo error: {exc}")
                    break
            except Exception as exc:
                logger.error(f"DuckDuckGo unexpected error: {exc}")
                break

        logger.warning("DuckDuckGo exhausted retries, returning empty results.")
        return []


class SerperSearch:
    def __init__(self, max_results: int = 5):
        self._max_results = max_results

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), reraise=True)
    def _do_search(self, query: str) -> dict:
        response = httpx.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": settings.SERPER_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "q": query,
                "num": self._max_results,
            },
            timeout=settings.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def search(self, query: str) -> List[SearchResult]:
        logger.info(f"Serper search: '{query}'")

        if not settings.SERPER_API_KEY or settings.SERPER_API_KEY == "YOUR_SERPER_API_KEY_HERE":
            logger.error("SERPER_API_KEY is not configured. Set it in .env.")
            return []

        try:
            data = self._do_search(query)
        except httpx.HTTPStatusError as exc:
            logger.error(f"Serper API error ({exc.response.status_code}): {exc.response.text}")
            return []
        except Exception as exc:
            logger.error(f"Serper search failed: {exc}")
            return []

        return [
            SearchResult(
                title=r.get("title", ""),
                url=r.get("link", ""),
                snippet=r.get("snippet", ""),
            )
            for r in data.get("organic", [])
        ]



_SEARCH_PROVIDERS = {
    "duckduckgo": DuckDuckGoSearch,
    "serper": SerperSearch,
}


def get_search_tool(max_results: int | None = None):
    provider = settings.SEARCH_PROVIDER.lower()
    cls = _SEARCH_PROVIDERS.get(provider)
    if cls is None:
        raise ValueError(f"Unsupported search provider '{provider}'. Supported: {list(_SEARCH_PROVIDERS.keys())}")
    return cls(max_results=max_results or settings.MAX_SEARCH_RESULTS)
