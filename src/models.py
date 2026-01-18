"""Data models for NewsApp - core data structures."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime


class Category(str, Enum):
    """News categories supported by NewsApp."""
    
    # Breaking news
    BREAKING = "breaking"
    
    # Agentic AI Categories
    AGENTIC_AI_DEV = "agentic_ai_dev"
    AGENTIC_AI_BUS = "agentic_ai_business"
    
    # Core news categories
    US = "us"
    WORLD = "world"
    
    # Technology & Business
    TECH = "tech"
    BUSINESS = "business"
    DEALS = "deals"
    
    # Lifestyle & Entertainment
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"
    SCIENCE = "science"
    
    # Industrial & Specialized
    MANUFACTURING = "manufacturing"
    LIFE_SCIENCES = "life_sciences"
    AUTOMOTIVE = "automotive"
    AVIATION = "aviation"
    
    # Emerging Technologies
    ECOMMERCE = "ecommerce"
    AGENTIC_AI = "agentic_ai"
    
    def __str__(self) -> str:
        """Return readable category name."""
        return self.value.replace("_", " ").title()


@dataclass
class FeedConfig:
    """Configuration for a single news feed."""
    
    name: str
    url: str
    feed_type: str  # "rss", "atom", or "scrape"
    category: Optional[str] = None
    enabled: bool = True
    timeout: int = 10


@dataclass
class Article:
    """Represents a single news article."""
    
    id: str  # Unique identifier
    headline: str
    summary: str
    source: str
    category: Category
    url: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    read_time_minutes: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    
    # Local flags
    is_read: bool = False
    is_bookmarked: bool = False
    cached_at: Optional[datetime] = None
    
    def __hash__(self):
        """Allow use as dict key."""
        return hash(self.id)


@dataclass
class AppState:
    """Global application state."""
    
    current_category: Category = Category.US
    articles: List[Article] = field(default_factory=list)
    selected_article: Optional[Article] = None
    related_articles: List[Article] = field(default_factory=list)
    view_mode: str = "dashboard"  # "dashboard" or "detail"
    is_loading: bool = False
    status_message: str = ""
    last_refresh: Optional[datetime] = None


@dataclass
class CacheMetadata:
    """Metadata about cached content."""
    
    category: str
    source: str
    fetched_at: datetime
    article_count: int
    refresh_interval_hours: int = 24
