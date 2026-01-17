"""SQLite-based cache manager for NewsApp."""

import sqlite3
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import json
from pathlib import Path

from ..models import Article, Category

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple SQLite-backed cache for articles."""

    def __init__(self, db_path: str = ".newsapp/cache.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self):
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                headline TEXT,
                summary TEXT,
                source TEXT,
                category TEXT,
                url TEXT,
                author TEXT,
                published_at TEXT,
                image_url TEXT,
                content TEXT,
                read_time INTEGER,
                tags TEXT,
                is_read INTEGER DEFAULT 0,
                is_bookmarked INTEGER DEFAULT 0,
                cached_at TEXT
            )
            """
        )
        self._conn.commit()

    def save_articles(self, articles: List[Article]):
        cur = self._conn.cursor()
        for a in articles:
            cur.execute(
                """
                INSERT OR REPLACE INTO articles (id, headline, summary, source, category, url, author,
                published_at, image_url, content, read_time, tags, is_read, is_bookmarked, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    a.id,
                    a.headline,
                    a.summary,
                    a.source,
                    a.category.value if isinstance(a.category, Category) else str(a.category),
                    a.url,
                    a.author,
                    a.published_at.isoformat() if a.published_at else None,
                    a.image_url,
                    a.content,
                    a.read_time_minutes,
                    json.dumps(a.tags),
                    1 if a.is_read else 0,
                    1 if a.is_bookmarked else 0,
                    (a.cached_at or datetime.utcnow()).isoformat(),
                ),
            )
        self._conn.commit()

    def get_articles(self, category: Optional[Category] = None, max_age_hours: Optional[int] = None, limit: int = 50) -> List[Article]:
        cur = self._conn.cursor()
        q = "SELECT * FROM articles"
        params = []
        clauses = []
        if category:
            clauses.append("category = ?")
            params.append(category.value if isinstance(category, Category) else str(category))
        if max_age_hours is not None:
            cutoff = (datetime.utcnow() - timedelta(hours=max_age_hours)).isoformat()
            clauses.append("cached_at >= ?")
            params.append(cutoff)
        if clauses:
            q += " WHERE " + " AND ".join(clauses)
        q += " ORDER BY published_at DESC LIMIT ?"
        params.append(limit)
        cur.execute(q, params)
        rows = cur.fetchall()
        articles: List[Article] = []
        for r in rows:
            published_at = None
            if r['published_at']:
                try:
                    published_at = datetime.fromisoformat(r['published_at'])
                except Exception:
                    published_at = None
            tags = json.loads(r['tags']) if r['tags'] else []
            article = Article(
                id=r['id'],
                headline=r['headline'],
                summary=r['summary'],
                source=r['source'],
                category=Category(r['category']) if r['category'] else Category.US,
                url=r['url'],
                author=r['author'],
                published_at=published_at,
                image_url=r['image_url'],
                content=r['content'],
                read_time_minutes=r['read_time'],
                tags=tags,
                is_read=bool(r['is_read']),
                is_bookmarked=bool(r['is_bookmarked']),
                cached_at=datetime.fromisoformat(r['cached_at']) if r['cached_at'] else None,
            )
            articles.append(article)
        return articles

    def mark_as_read(self, article_id: str, read: bool = True):
        cur = self._conn.cursor()
        cur.execute("UPDATE articles SET is_read = ? WHERE id = ?", (1 if read else 0, article_id))
        self._conn.commit()

    def mark_as_bookmarked(self, article_id: str, bookmarked: bool = True):
        cur = self._conn.cursor()
        cur.execute("UPDATE articles SET is_bookmarked = ? WHERE id = ?", (1 if bookmarked else 0, article_id))
        self._conn.commit()

    def get_bookmarked_articles(self, limit: int = 50) -> List[Article]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM articles WHERE is_bookmarked = 1 ORDER BY published_at DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        articles: List[Article] = []
        for r in rows:
            published_at = None
            if r['published_at']:
                try:
                    published_at = datetime.fromisoformat(r['published_at'])
                except Exception:
                    published_at = None
            tags = json.loads(r['tags']) if r['tags'] else []
            article = Article(
                id=r['id'],
                headline=r['headline'],
                summary=r['summary'],
                source=r['source'],
                category=Category(r['category']) if r['category'] else Category.US,
                url=r['url'],
                author=r['author'],
                published_at=published_at,
                image_url=r['image_url'],
                content=r['content'],
                read_time_minutes=r['read_time'],
                tags=tags,
                is_read=bool(r['is_read']),
                is_bookmarked=bool(r['is_bookmarked']),
                cached_at=datetime.fromisoformat(r['cached_at']) if r['cached_at'] else None,
            )
            articles.append(article)
        return articles

    def clear_old_articles(self, older_than_days: int = 30):
        cutoff = (datetime.utcnow() - timedelta(days=older_than_days)).isoformat()
        cur = self._conn.cursor()
        cur.execute("DELETE FROM articles WHERE cached_at < ?", (cutoff,))
        self._conn.commit()

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass
