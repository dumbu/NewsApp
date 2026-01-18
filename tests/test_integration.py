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
        
        # Should get articles from a reliable feed like HN
        assert isinstance(articles, list)
        assert len(articles) > 0, "Expected to fetch at least one article from HN RSS feed"
        
        # Validate article structure and content
        article = articles[0]
        assert article.id, "Article should have an ID"
        assert article.headline, "Article should have a headline"
        assert len(article.headline) > 5, "Article headline should have meaningful content"
        assert article.url.startswith('http'), "Article URL should be valid"
        assert article.category == Category.TECH, "Article should have correct category"
        assert article.source, "Article should have a source"
        
        # Validate content exists
        assert article.summary or article.content, "Article should have summary or content"
        if article.summary:
            assert len(article.summary) > 10, "Article summary should have meaningful content"
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fetch_multiple_feeds(self):
        """Test fetching from multiple feeds successfully."""
        handler = NewsHandler()
        
        # Use multiple reliable feeds
        feeds = [
            {"name": "HN", "url": "https://news.ycombinator.com/rss"},
            {"name": "Reddit", "url": "https://www.reddit.com/r/technology/.rss"}
        ]
        
        articles = await handler.fetch_category(
            feeds=feeds,
            scraping=[],
            category=Category.TECH,
            limit_per_source=3
        )
        
        # Should get articles from at least one feed
        assert isinstance(articles, list)
        assert len(articles) > 0, "Expected to fetch articles from at least one feed"
        
        # Validate all articles have required content
        for article in articles:
            assert article.headline, f"Article {article.id} missing headline"
            assert len(article.headline) > 5, f"Article {article.id} headline too short"
            assert article.url, f"Article {article.id} missing URL"
            assert article.source, f"Article {article.id} missing source"
            assert article.summary or article.content, f"Article {article.id} missing content"
        
        # Check for diversity of sources
        sources = {article.source for article in articles}
        assert len(sources) > 0, "Should have at least one unique source"
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_all_configured_categories_fetch_news(self):
        """Test that all configured categories can successfully fetch news."""
        config = ConfigManager()
        handler = NewsHandler()
        
        # Test ALL categories including new ones
        categories_to_test = [
            Category.BREAKING,
            Category.AGENTIC_AI_DEV,
            Category.AGENTIC_AI_BUS,
            Category.US,
            Category.WORLD,
            Category.TECH,
            Category.BUSINESS,
            Category.SCIENCE
        ]
        
        failed_categories = []
        
        for category in categories_to_test:
            feeds = config.get_feeds_for_category(category.value)
            
            # Skip if no feeds configured (expected for some categories)
            if not feeds:
                failed_categories.append((category.value, "No feeds configured"))
                continue
            
            try:
                articles = await handler.fetch_category(
                    feeds=feeds,
                    scraping=[],
                    category=category,
                    limit_per_source=3
                )
                
                if not articles or len(articles) == 0:
                    failed_categories.append((category.value, "No articles fetched - feeds may be broken"))
                else:
                    # Validate article content quality
                    article = articles[0]
                    
                    # Check for required fields
                    if not article.headline:
                        failed_categories.append((category.value, "Articles missing headlines"))
                    elif not article.url:
                        failed_categories.append((category.value, "Articles missing URLs"))
                    elif not article.source:
                        failed_categories.append((category.value, "Articles missing source"))
                    elif not (article.summary or article.content):
                        failed_categories.append((category.value, "Articles missing content/summary"))
                    
            except Exception as e:
                failed_categories.append((category.value, f"Error fetching: {str(e)[:50]}"))
        
        # Report all failures
        if failed_categories:
            error_msg = "\n❌ The following categories failed to fetch valid news content:\n"
            for cat, reason in failed_categories:
                error_msg += f"  - {cat}: {reason}\n"
            error_msg += "\nPlease fix RSS feeds or add valid sources for these categories."
            pytest.fail(error_msg)
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_category_with_no_feeds_returns_empty(self):
        """Test that categories with no configured feeds return empty list."""
        handler = NewsHandler()
        
        articles = await handler.fetch_category(
            feeds=[],
            scraping=[],
            category=Category.TECH,
            limit_per_source=5
        )
        
        assert isinstance(articles, list)
        assert len(articles) == 0, "Should return empty list when no feeds configured"


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
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_real_fetch_cache_retrieve_flow(self):
        """Test the full flow with actual news fetching."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up components
            db_path = Path(tmpdir) / "cache.db"
            cache = CacheManager(db_path=str(db_path))
            handler = NewsHandler()
            
            # Fetch real articles
            feeds = [{"name": "HN", "url": "https://news.ycombinator.com/rss"}]
            articles = await handler.fetch_category(
                feeds=feeds,
                scraping=[],
                category=Category.TECH,
                limit_per_source=5
            )
            
            # Should have fetched articles
            assert len(articles) > 0, "Should fetch real articles from HN"
            
            # Validate fetched articles have content
            for article in articles:
                assert article.headline, "Fetched article should have headline"
                assert article.url, "Fetched article should have URL"
                assert article.summary or article.content, "Fetched article should have content"
            
            # Save to cache
            cache.save_articles(articles)
            
            # Retrieve from cache
            cached_articles = cache.get_articles(
                category=Category.TECH,
                max_age_hours=1,
                limit=10
            )
            
            # Verify cached articles match fetched articles
            assert len(cached_articles) > 0, "Should have cached articles"
            assert len(cached_articles) <= len(articles), "Cached count should not exceed fetched count"
            
            # Verify cached articles retained content
            for article in cached_articles:
                assert article.headline, "Cached article should have headline"
                assert article.url, "Cached article should have URL"
                assert article.summary or article.content, "Cached article should have content"
            
            # Verify article integrity
            cached_ids = {a.id for a in cached_articles}
            original_ids = {a.id for a in articles}
            assert cached_ids.issubset(original_ids), "Cached articles should match original articles"
