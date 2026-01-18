"""Tests for API/news fetching functionality."""

import pytest
from src.api import NewsHandler
from src.models import Category


class TestNewsHandler:
    """Tests for NewsHandler."""
    
    @pytest.fixture
    def news_handler(self):
        """Create a NewsHandler instance."""
        return NewsHandler()
    
    def test_news_handler_initialization(self, news_handler):
        """Test NewsHandler initializes successfully."""
        assert news_handler is not None
    
    @pytest.mark.asyncio
    async def test_fetch_category_with_empty_feeds(self, news_handler):
        """Test fetching with no feeds returns empty list."""
        articles = await news_handler.fetch_category(
            feeds=[],
            scraping=[],
            category=Category.TECH,
            limit_per_source=5
        )
        assert isinstance(articles, list)
        assert len(articles) == 0
    
    @pytest.mark.asyncio
    async def test_fetch_category_with_invalid_feed(self, news_handler):
        """Test fetching with invalid feed handles errors gracefully."""
        invalid_feeds = [
            {"name": "invalid", "url": "https://invalid-url-that-does-not-exist-12345.com/feed"}
        ]
        
        articles = await news_handler.fetch_category(
            feeds=invalid_feeds,
            scraping=[],
            category=Category.TECH,
            limit_per_source=5
        )
        
        # Should not crash, should return empty or partial results
        assert isinstance(articles, list)
