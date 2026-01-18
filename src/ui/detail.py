"""Detail view for NewsApp articles."""

from typing import List
import webbrowser

from textual.widgets import Static
from textual.containers import ScrollableContainer
from ..models import Article


class ArticleDetailsPanel(Static):
    def __init__(self, article: Article):
        super().__init__()
        self.article = article
        self.render()

    def render(self):
        head = f"{self.article.headline}\n{self.article.source} - {self.article.published_at}\n"
        meta = f"By: {self.article.author or 'Unknown'} | Tags: {', '.join(self.article.tags)}\n"
        self.update(head + meta)


class ArticleContentView(ScrollableContainer):
    def __init__(self, article: Article):
        super().__init__()
        self.article = article
        self.update_content()

    def update_content(self):
        content = self.article.content or self.article.summary or "(no content)"
        self.update(content)


class RelatedArticlesList(Static):
    def __init__(self, related: List[Article]):
        super().__init__()
        self.related = related
        self.update(self._render_list())

    def _render_list(self) -> str:
        lines = []
        for i, a in enumerate(self.related, 1):
            lines.append(f"{i}. {a.headline} ({a.source})")
        return "\n".join(lines)


class DetailView(Static):
    def __init__(self, article: Article, related: List[Article]):
        super().__init__()
        self.article = article
        self.related = related
        self.details = ArticleDetailsPanel(article)
        self.content = ArticleContentView(article)
        self.related_list = RelatedArticlesList(related)
        self._build()

    def _build(self):
        self.update(self.details.renderable)
        # Textual layouting can be improved, keep simple for now

    def open_in_browser(self):
        webbrowser.open(self.article.url)
