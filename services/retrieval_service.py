import logging
from dataclasses import dataclass
from typing import List

from tools.search_tool import SearchResult, get_search_tool
from tools.webpage_loader import load_page_content

logger = logging.getLogger(__name__)


@dataclass
class RetrievedContext:
    content: str
    source_url: str
    title: str


class RetrievalService:
    def __init__(self, max_results: int | None = None):
        self._search = get_search_tool(max_results)

    def retrieve(self, query: str) -> List[RetrievedContext]:
        results: List[SearchResult] = self._search.search(query)
        contexts: List[RetrievedContext] = []

        for result in results:
            page_text = load_page_content(result.url)
            content = page_text if page_text else result.snippet

            contexts.append(
                RetrievedContext(
                    content=content,
                    source_url=result.url,
                    title=result.title,
                )
            )

        logger.info(f"Retrieved {len(contexts)} context blocks for query: '{query}'")
        return contexts
