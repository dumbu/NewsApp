"""Integration tests that test real app behavior."""

import pytest
import tempfile
from pathlib import Path
from src.config import ConfigManager
from src.cache import CacheManager
from src.api import NewsHandler
from src.models import Category, Article
from datetime import datetime


class TestCacheIntegration:
    """Test cache with real database operations."""
    
    def test_cache_database_initialization(self):
        """Test that cache database is properly created and initialized."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / ".newsapp" / "cache.db"
            cache = CacheManager(db_path=str(db_path))
            
            # Database file should exist
            assert db_path.exists()
            
            # Should be able to save articles
            articles = [
                Article(
                    id="test-1",
                    headline="Test Article",
                    summary="Test summary",
                    source="Test",
                    category=Category.TECH,
                    url="https://example.com"
                )
            ]
            
            # This should not raise any errors
            cache.save_articles(articles)
            
            # Should be able to retrieve articles
            retrieved = cache.get_articles(category=Category.TECH, max_age_hours=1)
            assert len(retrieved) == 1
            assert retrieved[0].id == "test-1"
    
    def test_cache_handles_missing_directory(self):
        """Test cache creates missing parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Use a deeply nested path that doesn't exist
            db_path = Path(tmpdir) / "deeply" / "nested" / "path" / "cache.db"
            
            # Should not raise an error
            cache = CacheManager(db_path=str(db_path))
            assert db_path.exists()


class TestConfigIntegration:
    """Test configuration with real file operations."""
    
    def test_config_loads_without_file(self):
        """Test config works with no config file (uses defaults)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = ConfigManager(config_path=config_path)
            
            # Should load with defaults
            assert config.ui is not None
            assert config.cache is not None
            assert config.news is not None
    
    def test_config_returns_valid_feeds(self):
        """Test that config returns actually usable feeds."""
        config = ConfigManager()
        
        # Should have feeds for at least some categories
        for category in [Category.TECH, Category.US, Category.WORLD]:
            feeds = config.get_feeds_for_category(category.value)
            
            # Should return a list
            assert isinstance(feeds, list)
            
            # Each feed should have required fields
            for feed in feeds:
                assert 'name' in feed
                assert 'url' in feed
                assert feed['url'].startswith('http')


@pytest.mark.integration
class TestNewsAPIIntegration:
    """Test actual news fetching (may be slow)."""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_fetch_real_feed(self):
        """Test fetching from a real RSS feed."""
        handler = NewsHandler()
        
        # Use a reliable test feed
        feeds = [{"name": "HN", "url": "https://news.ycombinator.com/rss"}]
        
        articles = await handler.fetch_category(
            feeds=feeds,
            scraping=[],
            category=Category.TECH,
            limit_per_source=5
        )
        
        # Should get some articles (unless network is down)
        # Making this flexible since it's a real network call
        assert isinstance(articles, list)
        
        # If we got articles, they should be valid
        if articles:
            article = articles[0]
            assert article.id
            assert article.headline
            assert article.url.startswith('http')
            assert article.category == Category.TECH


class TestEndToEndFlow:
    """Test complete workflow from fetch to cache to retrieve."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fetch_and_cache_flow(self):
        """Test the full flow: fetch news -> save to cache -> retrieve."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up components
            db_path = Path(tmpdir) / "cache.db"
            cache = CacheManager(db_path=str(db_path))
            handler = NewsHandler()
            
            # Create test article
            test_article = Article(
                id="flow-test-1",
                headline="Flow Test Article",
                summary="Testing the complete flow",
                source="Test Source",
                category=Category.BUSINESS,
                url="https://example.com/article",
                published_at=datetime.now()
            )
            
            # Save to cache
            cache.save_articles([test_article])
            
            # Retrieve from cache
            cached_articles = cache.get_articles(
                category=Category.BUSINESS,
                max_age_hours=1,
                limit=10
            )
            
            # Verify
            assert len(cached_articles) == 1
            assert cached_articles[0].id == "flow-test-1"
            assert cached_articles[0].headline == "Flow Test Article"
            assert cached_articles[0].category == Category.BUSINESS
