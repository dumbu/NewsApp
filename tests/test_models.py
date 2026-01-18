"""Tests for data models."""

import pytest
from datetime import datetime
from src.models import Article, Category, AppState, FeedConfig


class TestCategory:
    """Tests for Category enum."""
    
    def test_category_values(self):
        """Test category enum values."""
        assert Category.BREAKING.value == "breaking"
        assert Category.AGENTIC_AI_DEV.value == "agentic_ai_dev"
        assert Category.AGENTIC_AI_BUS.value == "agentic_ai_business"
        assert Category.US.value == "us"
        assert Category.TECH.value == "tech"
        assert Category.WORLD.value == "world"
    
    def test_category_string_representation(self):
        """Test category string representation."""
        assert str(Category.US) == "Us"
        assert str(Category.TECH) == "Tech"
        assert str(Category.AGENTIC_AI) == "Agentic Ai"
        assert str(Category.BREAKING) == "Breaking"


class TestArticle:
    """Tests for Article model."""
    
    def test_article_creation(self, sample_article):
        """Test creating an article."""
        assert sample_article.id == "test-123"
        assert sample_article.headline == "Test Article Headline"
        assert sample_article.category == Category.TECH
        assert sample_article.is_read is False
        assert sample_article.is_bookmarked is False
    
    def test_article_hash(self, sample_article):
        """Test article can be used in sets/dicts."""
        article_set = {sample_article}
        assert sample_article in article_set
    
    def test_article_tags(self, sample_article):
        """Test article tags."""
        assert "test" in sample_article.tags
        assert "sample" in sample_article.tags
        assert len(sample_article.tags) == 2


class TestFeedConfig:
    """Tests for FeedConfig model."""
    
    def test_feed_config_creation(self):
        """Test creating a feed config."""
        feed = FeedConfig(
            name="Test Feed",
            url="https://example.com/feed.xml",
            feed_type="rss",
            category="tech"
        )
        assert feed.name == "Test Feed"
        assert feed.enabled is True
        assert feed.timeout == 10


class TestAppState:
    """Tests for AppState model."""
    
    def test_app_state_defaults(self):
        """Test default app state."""
        state = AppState()
        assert state.current_category == Category.US
        assert state.articles == []
        assert state.selected_article is None
        assert state.view_mode == "dashboard"
        assert state.is_loading is False
    
    def test_app_state_with_articles(self, sample_articles):
        """Test app state with articles."""
        state = AppState(articles=sample_articles)
        assert len(state.articles) == 5
        assert state.articles[0].id == "test-0"
