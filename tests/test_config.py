"""Tests for configuration management."""

import pytest
import yaml
from pathlib import Path
from src.config import ConfigManager, UIConfig, CacheConfig, NewsConfig
from src.models import Category


class TestUIConfig:
    """Tests for UI configuration."""
    
    def test_ui_config_defaults(self):
        """Test default UI config values."""
        config = UIConfig()
        assert config.theme == "dark"
        assert config.color_mode is True
        assert config.columns == 3
        assert config.max_headline_length == 80


class TestCacheConfig:
    """Tests for cache configuration."""
    
    def test_cache_config_defaults(self):
        """Test default cache config values."""
        config = CacheConfig()
        assert config.enabled is True
        assert config.ttl == 86400
        assert config.max_articles == 1000


class TestNewsConfig:
    """Tests for news configuration."""
    
    def test_news_config_defaults(self):
        """Test default news config values."""
        config = NewsConfig()
        assert config.rss_feeds is not None
        assert config.scraping_sources is not None
        assert isinstance(config.rss_feeds, dict)
    
    def test_default_rss_feeds(self):
        """Test default RSS feeds are loaded."""
        config = NewsConfig()
        feeds = config._default_rss_feeds()
        assert "hackernews" in feeds
        assert "techcrunch" in feeds
        assert feeds["hackernews"]["url"] == "https://news.ycombinator.com/rss"


class TestConfigManager:
    """Tests for ConfigManager."""
    
    def test_config_manager_initialization(self, config_manager):
        """Test ConfigManager initializes with defaults."""
        assert config_manager.ui is not None
        assert config_manager.cache is not None
        assert config_manager.news is not None
    
    def test_get_feeds_for_category(self, config_manager):
        """Test getting feeds for a category."""
        feeds = config_manager.get_feeds_for_category("tech")
        assert isinstance(feeds, list)
        # Should have at least some tech feeds
        assert len(feeds) > 0
        # Each feed should have name and url
        for feed in feeds:
            assert "name" in feed
            assert "url" in feed
    
    def test_get_feeds_for_empty_category(self, config_manager):
        """Test getting feeds for non-existent category."""
        feeds = config_manager.get_feeds_for_category("nonexistent")
        assert isinstance(feeds, list)
        assert len(feeds) == 0
    
    def test_save_and_load_config(self, temp_config_dir):
        """Test saving and loading configuration."""
        config_file = temp_config_dir / "config.yaml"
        
        # Create and save config
        config1 = ConfigManager(config_path=config_file)
        config1.ui.max_headline_length = 100
        config1.save_config()
        
        # Load config in new instance
        config2 = ConfigManager(config_path=config_file)
        assert config2.ui.max_headline_length == 100
    
    def test_get_scraping_sources_for_category(self, config_manager):
        """Test getting scraping sources for a category."""
        sources = config_manager.get_scraping_sources_for_category("tech")
        assert isinstance(sources, list)
        # Each source should have required fields
        for source in sources:
            assert "name" in source
            assert "url" in source
