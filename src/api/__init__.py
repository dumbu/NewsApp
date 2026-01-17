"""News fetching utilities: RSS parsing and light scraping."""

import asyncio
from datetime import datetime
from typing import List, Dict, Optional
import logging

import aiohttp
import feedparser
from bs4 import BeautifulSoup

from ..models import Article, FeedConfig, Category

logger = logging.getLogger(__name__)


class NewsHandler:
    """Fetch articles from RSS feeds and scraping sources."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._external_session = session

    async def _fetch_text(self, url: str, timeout: int = 10) -> Optional[str]:
        session = self._external_session or aiohttp.ClientSession()
        try:
            async with session.get(url, timeout=timeout) as resp:
                if resp.status != 200:
                    logger.warning(f"Failed to fetch {url}: {resp.status}")
                    return None
                return await resp.text()
        except Exception as e:
            logger.exception(f"Error fetching {url}: {e}")
            return None
        finally:
            if not self._external_session:
                await session.close()

    async def fetch_from_rss(self, feed_url: str, source_name: str, category: Category, limit: int = 20) -> List[Article]:
        """Fetch articles from an RSS feed URL."""
        text = await self._fetch_text(feed_url)
        if not text:
            logger.debug(f"No text returned from {feed_url}")
            return []

        try:
            parsed = feedparser.parse(text)
            if parsed.bozo:
                logger.debug(f"Feed parse warning from {source_name}: {parsed.bozo_exception}")
            
            articles: List[Article] = []
            for entry in parsed.entries[:limit]:
                article_id = entry.get('id') or entry.get('link') or entry.get('title')
                published_parsed = entry.get('published_parsed')
                published_at = None
                if published_parsed:
                    published_at = datetime(*published_parsed[:6])

                summary = entry.get('summary') or entry.get('description') or ''
                article = Article(
                    id=str(article_id),
                    headline=entry.get('title', '')[:300],
                    summary=summary[:1000],
                    source=source_name,
                    category=category,
                    url=entry.get('link', ''),
                    author=entry.get('author'),
                    published_at=published_at,
                )
                articles.append(article)
            
            if articles:
                logger.debug(f"Fetched {len(articles)} articles from {source_name}")
            return articles
        except Exception as e:
            logger.error(f"Error parsing feed from {source_name}: {e}")
            return []

    async def fetch_from_scrape(self, url: str, selector: str, source_name: str, category: Category, limit: int = 20) -> List[Article]:
        """A minimal scraping path using BeautifulSoup selectors."""
        text = await self._fetch_text(url)
        if not text:
            return []

        soup = BeautifulSoup(text, 'lxml')
        results = soup.select(selector)
        articles: List[Article] = []
        for el in results[:limit]:
            a = el.find('a') if el.name != 'a' else el
            if not a or not a.get('href'):
                continue
            title = a.get_text(strip=True)
            href = a.get('href')
            # Normalize relative URLs
            if href.startswith('/'):
                href = url.rstrip('/') + href
            article = Article(
                id=href,
                headline=title[:300],
                summary='(scraped)',
                source=source_name,
                category=category,
                url=href,
            )
            articles.append(article)
        return articles

    async def fetch_category(self, feeds: List[Dict], scraping: List[Dict], category: Category, limit_per_source: int = 10) -> List[Article]:
        """Fetch from multiple feed sources and scraping sources concurrently."""
        tasks = []
        for f in feeds:
            tasks.append(self.fetch_from_rss(f['url'], f.get('name', 'rss'), category, limit_per_source))
        for s in scraping:
            selector = s.get('selectors')
            # If selectors is a dict, pick first selector value
            sel = None
            if isinstance(selector, dict):
                sel = next(iter(selector.keys()), None)
            elif isinstance(selector, str):
                sel = selector
            if sel:
                tasks.append(self.fetch_from_scrape(s['url'], sel, s.get('name', 'scrape'), category, limit_per_source))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        articles: List[Article] = []
        seen = set()
        for r in results:
            if isinstance(r, Exception):
                logger.exception("Error in fetch task", exc_info=r)
                continue
            for a in r:
                if a.id in seen:
                    continue
                seen.add(a.id)
                articles.append(a)
        return articles

    async def fetch_article_content(self, article: Article) -> Optional[str]:
        """Fetch and populate full content for an article."""
        text = await self._fetch_text(article.url)
        if not text:
            return None
        soup = BeautifulSoup(text, 'lxml')
        # Try common article selectors
        selectors = ['article', '.article-body', '.post-content', '.entry-content']
        content = None
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                content = el.get_text(separator='\n', strip=True)
                break
        if not content:
            content = soup.get_text(separator='\n', strip=True)[:20000]
        article.content = content
        return content
