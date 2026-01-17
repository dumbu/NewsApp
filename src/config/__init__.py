"""Configuration management for NewsApp."""

import os
import yaml
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import logging


logger = logging.getLogger(__name__)


@dataclass
class UIConfig:
    """UI configuration."""
    
    theme: str = "dark"
    color_mode: bool = True
    columns: int = 3
    show_source_icons: bool = True
    max_headline_length: int = 80
    date_format: str = "%b %d, %H:%M"
    refresh_interval: int = 300  # seconds
    headline_limit: int = 20
    auto_refresh: bool = True


@dataclass
class CacheConfig:
    """Cache configuration."""
    
    enabled: bool = True
    location: str = ".newsapp/cache.db"
    ttl: int = 86400  # 24 hours in seconds
    max_articles: int = 1000


@dataclass
class LogConfig:
    """Logging configuration."""
    
    level: str = "INFO"
    file: Optional[str] = None
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class NewsConfig:
    """News source configuration."""
    
    rss_feeds: Dict[str, Dict[str, str]] = None
    scraping_sources: Dict[str, Dict[str, str]] = None
    api_key: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default feeds if not provided."""
        if self.rss_feeds is None:
            self.rss_feeds = self._default_rss_feeds()
        if self.scraping_sources is None:
            self.scraping_sources = self._default_scraping_sources()
    
    @staticmethod
    def _default_rss_feeds() -> Dict[str, Dict[str, str]]:
        """Return default RSS feed configuration."""
        return {
            "hackernews": {
                "url": "https://news.ycombinator.com/rss",
                "categories": ["tech", "business"],
            },
            "github_trending": {
                "url": "https://github.com/trending.atom",
                "categories": ["tech"],
            },
            "techcrunch": {
                "url": "https://techcrunch.com/feed/",
                "categories": ["tech", "business"],
            },
            "bbc_tech": {
                "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
                "categories": ["tech"],
            },
            "bbc_us": {
                "url": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
                "categories": ["us", "world"],
            },
            "bbc_world": {
                "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
                "categories": ["world"],
            },
            "bbc_business": {
                "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
                "categories": ["business"],
            },
            "bbc_science": {
                "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
                "categories": ["science"],
            },
            "bbc_sport": {
                "url": "https://feeds.bbci.co.uk/sport/rss.xml",
                "categories": ["sports"],
            },
            "bbc_entertainment": {
                "url": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
                "categories": ["entertainment"],
            },
            "npr_news": {
                "url": "https://feeds.npr.org/1001/rss.xml",
                "categories": ["us", "world"],
            },
            "reuters_world": {
                "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
                "categories": ["world", "business"],
            },
            "reddit_worldnews": {
                "url": "https://www.reddit.com/r/worldnews/.rss",
                "categories": ["world"],
            },
            "reddit_news": {
                "url": "https://www.reddit.com/r/news/.rss",
                "categories": ["us"],
            },
            "reddit_technology": {
                "url": "https://www.reddit.com/r/technology/.rss",
                "categories": ["tech"],
            },
        }
    
    @staticmethod
    def _default_scraping_sources() -> Dict[str, Dict[str, str]]:
        """Return default scraping source configuration."""
        return {}  # Disabled by default - scraping is unreliable


class ConfigManager:
    """Manage application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to YAML config file. If not provided,
                        uses config/config.yaml or creates from template.
        """
        self.config_path = Path(config_path) if config_path else self._find_config()
        self.ui = UIConfig()
        self.cache = CacheConfig()
        self.log = LogConfig()
        self.news = NewsConfig()
        
        self._load_config()
    
    def _find_config(self) -> Path:
        """Find config file, creating from template if needed."""
        # Check for config/config.yaml
        config_file = Path("config/config.yaml")
        if config_file.exists():
            return config_file
        
        # Check for config/config.template.yaml and use as default
        template_file = Path("config/config.template.yaml")
        if template_file.exists():
            return template_file
        
        # Default location
        return Path("config/config.yaml")
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found at {self.config_path}, using defaults")
            return
        
        try:
            with open(self.config_path, "r") as f:
                config_data = yaml.safe_load(f) or {}
            
            # Load UI config
            if "ui" in config_data:
                self.ui = UIConfig(**config_data["ui"])
            
            # Load cache config
            if "cache" in config_data:
                self.cache = CacheConfig(**config_data["cache"])
            
            # Load log config
            if "log" in config_data:
                self.log = LogConfig(**config_data["log"])
            
            # Load news config
            if "news" in config_data:
                news_data = config_data["news"]
                self.news = NewsConfig(
                    rss_feeds=news_data.get("rss_feeds", self.news.rss_feeds),
                    scraping_sources=news_data.get("scraping_sources", self.news.scraping_sources),
                    api_key=news_data.get("api_key"),
                )
            
            logger.info(f"Configuration loaded from {self.config_path}")
        
        except Exception as e:
            logger.error(f"Failed to load config: {e}, using defaults")
    
    def save_config(self) -> None:
        """Save current configuration to YAML file."""
        config_data = {
            "ui": asdict(self.ui),
            "cache": asdict(self.cache),
            "log": asdict(self.log),
            "news": {
                "rss_feeds": self.news.rss_feeds,
                "scraping_sources": self.news.scraping_sources,
                "api_key": self.news.api_key,
            }
        }
        
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                yaml.dump(config_data, f, default_flow_style=False)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get_feeds_for_category(self, category: str) -> List[Dict[str, str]]:
        """Get RSS feeds for a specific category.
        
        Args:
            category: Category name (e.g., "tech", "us")
        
        Returns:
            List of feed configurations matching the category
        """
        feeds = []
        for feed_name, feed_config in self.news.rss_feeds.items():
            if category in feed_config.get("categories", []):
                feeds.append({
                    "name": feed_name,
                    "url": feed_config["url"],
                })
        return feeds
    
    def get_scraping_sources_for_category(self, category: str) -> List[Dict]:
        """Get scraping sources for a specific category."""
        sources = []
        for source_name, source_config in self.news.scraping_sources.items():
            if category in source_config.get("categories", []):
                sources.append({
                    "name": source_name,
                    "url": source_config["url"],
                    "selectors": source_config.get("selectors", {}),
                })
        return sources
