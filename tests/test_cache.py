"""Tests for cache management."""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from src.cache import CacheManager
from src.models import Category


class TestCacheManager:
    """Tests for CacheManager."""
    
    @pytest.fixture
    def cache_manager(self):
        """Create a temporary cache manager for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            cache_path = tmp.name
        
        manager = CacheManager(db_path=cache_path)
        yield manager
        
        # Cleanup
        Path(cache_path).unlink(missing_ok=True)
    
    def test_cache_manager_initialization(self, cache_manager):
        """Test cache manager initializes successfully."""
        assert cache_manager is not None
    
    def test_save_and_get_articles(self, cache_manager, sample_articles):
        """Test saving and retrieving articles from cache."""
        # Save articles
        cache_manager.save_articles(sample_articles)
        
        # Retrieve articles
        cached = cache_manager.get_articles(
            category=Category.TECH,
            max_age_hours=1,
            limit=10
        )
        
        assert len(cached) == 5
        assert cached[0].id == "test-0"
    
    def test_get_expired_articles(self, cache_manager, sample_articles):
        """Test that expired articles are not returned."""
        # Save articles
        cache_manager.save_articles(sample_articles)
        
        # Try to get with max_age_hours=0 (should be expired)
        cached = cache_manager.get_articles(
            category=Category.TECH,
            max_age_hours=0,
            limit=10
        )
        
        # Should return empty list for expired cache
        assert len(cached) == 0
    
    def test_cache_limit(self, cache_manager, sample_articles):
        """Test cache respects limit parameter."""
        # Save 5 articles
        cache_manager.save_articles(sample_articles)
        
        # Get only 3
        cached = cache_manager.get_articles(
            category=Category.TECH,
            max_age_hours=1,
            limit=3
        )
        
        assert len(cached) == 3
    
    def test_get_articles_by_category(self, cache_manager, sample_articles):
        """Test getting articles filtered by category."""
        # Modify one article to have different category
        sample_articles[0].category = Category.BUSINESS
        cache_manager.save_articles(sample_articles)
        
        # Get only TECH articles
        tech_articles = cache_manager.get_articles(
            category=Category.TECH,
            max_age_hours=1,
            limit=10
        )
        
        # Should get 4 tech articles (5 - 1 business)
        assert len(tech_articles) == 4
        for article in tech_articles:
            assert article.category == Category.TECH
