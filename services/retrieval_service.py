import logging
from dataclasses import dataclass
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from tools.search_tool import SearchResult, get_search_tool
from tools.webpage_loader import load_page_content

logger = logging.getLogger(__name__)


@dataclass
class RetrievedContext:
    content: str
    source_url: str
    title: str


def _fetch_one(result: SearchResult) -> RetrievedContext:
    page_text = load_page_content(result.url)
    return RetrievedContext(
        content=page_text if page_text else result.snippet,
        source_url=result.url,
        title=result.title,
    )


class RetrievalService:
    def __init__(self, max_results: int | None = None):
        self._search = get_search_tool(max_results)

    def retrieve(self, query: str) -> List[RetrievedContext]:
        results: List[SearchResult] = self._search.search(query)
        if not results:
            return []

        # Fetch all pages concurrently
        contexts: List[RetrievedContext] = []
        with ThreadPoolExecutor(max_workers=len(results)) as pool:
            futures = {pool.submit(_fetch_one, r): r for r in results}
            for future in as_completed(futures):
                try:
                    contexts.append(future.result())
                except Exception as exc:
                    r = futures[future]
                    logger.warning(f"Page fetch failed for {r.url}: {exc}")
                    contexts.append(
                        RetrievedContext(
                            content=r.snippet,
                            source_url=r.url,
                            title=r.title,
                        )
                    )

        logger.info(f"Retrieved {len(contexts)} context blocks for query: '{query}'")
        return contexts
