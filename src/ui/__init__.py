"""Dashboard view components for NewsApp using Textual."""

from typing import List
import logging

from textual.widgets import Static, ListView, ListItem
from textual import events
from textual.reactive import Reactive

from ..models import Article

logger = logging.getLogger(__name__)


class ArticleListItem(ListItem):
    """List item representing a single article."""

    def __init__(self, article: Article):
        super().__init__()
        self.article = article
        self.refresh()

    def refresh(self):
        title = self.article.headline
        status = "🔖" if self.article.is_bookmarked else ("✓" if self.article.is_read else " ")
        self.set_label(f"{status} {title}")


class HeadlineListView(Static):
    """Container for article headlines."""

    articles: Reactive[List[Article]] = Reactive([])

    def __init__(self):
        super().__init__()
        self.list = ListView()

    def set_articles(self, articles: List[Article]):
        self.articles = articles
        self.list.clear()
        for a in articles:
            self.list.append(ArticleListItem(a))


class CategorySelector(Static):
    """Simple category selector (keyboard only)."""

    def on_key(self, event: events.Key):
        if event.key == "1":
            self.post_message("category_selected", "us")
        elif event.key == "2":
            self.post_message("category_selected", "world")
        elif event.key == "3":
            self.post_message("category_selected", "tech")
        elif event.key == "4":
            self.post_message("category_selected", "business")
        elif event.key == "5":
            self.post_message("category_selected", "science")


class StatusBar(Static):
    """Simple status bar for messages."""

    def set_message(self, msg: str):
        self.update(msg)
