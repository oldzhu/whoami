"""Web content fetcher — extracts text from any public URL for knowledge ingestion."""
import re
import logging
from typing import Optional, Dict
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Simple HTML tag stripper (no external dependency needed)
HTML_TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_STYLE_RE = re.compile(r"<(script|style|noscript|iframe)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
WHITESPACE_RE = re.compile(r"\s+")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")  # Markdown links


class WebContentFetcher:
    """Fetches and extracts readable text from public URLs."""

    @staticmethod
    async def fetch(url: str, timeout: int = 20) -> Optional[str]:
        """Fetch raw HTML content from a URL."""
        import aiohttp
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DigitalTwin/1.0; +https://github.com/oldzhu/whoami)",
            "Accept": "text/html,application/xhtml+xml,text/plain",
            "Accept-Language": "en,zh;q=0.9",
        }
        try:
            async with aiohttp.ClientSession(trust_env=False) as session:
                async with session.get(
                    url, headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    allow_redirects=True, max_redirects=3,
                ) as resp:
                    if resp.status == 200:
                        content_type = resp.headers.get("Content-Type", "")
                        if "text/html" in content_type:
                            return await resp.text()
                        elif "text/plain" in content_type or "text/markdown" in content_type:
                            return await resp.text()
                        elif "application/json" in content_type:
                            return await resp.text()
                        else:
                            logger.info(f"Skipping non-text content: {content_type[:50]}")
                            return None
                    else:
                        logger.info(f"HTTP {resp.status} for {url}")
                        return None
        except Exception as e:
            logger.info(f"Failed to fetch {url}: {e}")
            return None

    @staticmethod
    def extract_text(html: str, max_chars: int = 10000) -> str:
        """Extract readable text from HTML, stripping tags and scripts."""
        # Remove script/style/noscript blocks
        text = SCRIPT_STYLE_RE.sub(" ", html)
        # Remove HTML tags
        text = HTML_TAG_RE.sub(" ", text)
        # Decode common entities
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
        # Collapse whitespace
        text = WHITESPACE_RE.sub(" ", text).strip()
        # Truncate
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        return text

    @staticmethod
    def extract_title(html: str) -> str:
        """Extract page title from HTML."""
        match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if match:
            return HTML_TAG_RE.sub("", match.group(1)).strip()[:200]
        return ""

    @staticmethod
    async def extract(url: str) -> Dict:
        """Fetch a URL and extract structured content."""
        result = {
            "url": url,
            "title": "",
            "text": "",
            "domain": urlparse(url).netloc,
            "success": False,
        }

        html = await WebContentFetcher.fetch(url)
        if html is None:
            return result

        result["success"] = True
        result["title"] = WebContentFetcher.extract_title(html)
        result["text"] = WebContentFetcher.extract_text(html)
        return result
