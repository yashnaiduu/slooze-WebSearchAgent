import logging
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)

STRIPPED_TAGS = {"script", "style", "nav", "footer", "header", "aside", "form", "noscript"}


@retry(wait=wait_exponential(min=1, max=8), stop=stop_after_attempt(2), reraise=True)
def load_page_content(url: str, max_length: int | None = None) -> Optional[str]:
    max_length = max_length or settings.MAX_PAGE_CONTENT_LENGTH
    try:
        response = httpx.get(
            url,
            timeout=settings.REQUEST_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; AISearchBot/1.0)"},
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning(f"Failed to fetch {url}: {exc}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.find_all(STRIPPED_TAGS):
        tag.decompose()

    # prefer <article> or <main> content
    main = soup.find("article") or soup.find("main") or soup.find("body")
    if main is None:
        return None

    text = main.get_text(separator="\n", strip=True)
    if len(text) > max_length:
        text = text[:max_length] + "…"

    return text if text else None
