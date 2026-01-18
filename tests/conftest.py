"""Pytest configuration and shared fixtures."""

import pytest
import tempfile
from pathlib import Path
from src.config import ConfigManager
from src.models import Category, Article
from datetime import datetime


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for test config files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def config_manager(temp_config_dir):
    """Create a ConfigManager instance for testing."""
    config_file = temp_config_dir / "config.yaml"
    return ConfigManager(config_path=config_file)


@pytest.fixture
def sample_article():
    """Create a sample article for testing."""
    return Article(
        id="test-123",
        headline="Test Article Headline",
        summary="This is a test summary",
        source="Test Source",
        category=Category.TECH,
        url="https://example.com/article",
        author="Test Author",
        published_at=datetime.now(),
        tags=["test", "sample"]
    )


@pytest.fixture
def sample_articles():
    """Create multiple sample articles for testing."""
    return [
        Article(
            id=f"test-{i}",
            headline=f"Test Article {i}",
            summary=f"Summary {i}",
            source="Test Source",
            category=Category.TECH,
            url=f"https://example.com/article-{i}",
        )
        for i in range(5)
    ]
