"""Terminal News Application - Main Entry Point"""

import sys
import asyncio
import logging

from textual.app import ComposeResult, App
from textual.widgets import Header, Footer, Static, Button, Label
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.message import Message

from .config import ConfigManager
from .api import NewsHandler
from .cache import CacheManager
from .models import AppState, Category, Article
from .ui.settings import SettingsView, BackToDashboardMessage


logger = logging.getLogger(__name__)


class NewsAppUI(App):
    """Main Textual application for NewsApp."""
    
    TITLE = "Terminal News Application"
    SUBTITLE = "v0.1.0"
    
    CSS = """
    #main-container {
        height: 1fr;
        layout: vertical;
    }
    
    #content-area {
        height: 1fr;
        layout: horizontal;
    }
    
    #top-bar {
        height: 3;
        background: $boost;
    }
    
    #categories-panel {
        width: 27;
        border: solid $accent;
        background: $panel;
        padding: 0;
        margin: 0;
    }
    
    #categories-panel Button {
        width: 100%;
    }
    
    #categories-header {
        background: $boost;
        padding: 0 1;
        height: 3;
    }
    
    #articles-panel {
        width: 1fr;
        border: solid $accent;
        background: $panel;
        padding: 0;
        margin: 0;
    }
    
    #articles-list {
        width: 1fr;
        height: auto;
    }
    
    Button {
        margin: 0 0;
    }
    
    .article-btn {
        width: 100%;
        height: auto;
        text-align: left;
        margin: 0 0 1 0;
    }
    
    .url-btn {
        width: 100%;
        margin: 1 0;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.cfg = ConfigManager()
        self.cache = CacheManager(db_path=self.cfg.cache.location)
        self.handler = NewsHandler()
        self.state = AppState()
        self.articles = []
        self.current_view = "dashboard"  # "dashboard" or "settings"
        self.article_view_mode = "list"  # "list" or "detail"
        self.selected_article = None
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            # Two-column layout: categories on left, content on right
            with Horizontal(id="content-area"):
                # Left panel: Categories
                with Vertical(id="categories-panel"):
                    yield Label("📂 Categories", id="categories-header")
                    yield Button("🌟 Breaking News", id="cat-breaking")
                    yield Button("🤖 Agentic AI Developer", id="cat-agentic-dev")
                    yield Button("💼 Agentic AI Business", id="cat-agentic-bus")
                    yield Button("🗽 US News", id="cat-us")
                    yield Button("🌍 World", id="cat-world")
                    yield Button("💻 Tech", id="cat-tech")
                    yield Button("💼 Business", id="cat-business")
                    yield Button("🔬 Science", id="cat-science")
                
                # Right panel: Articles content
                with ScrollableContainer(id="articles-panel"):
                    yield Static("Select a category to view articles", id="articles-list")
            
            # Bottom bar with controls
            with Horizontal(id="top-bar"):
                yield Button("⚙️  [b][cyan]S[/cyan][/b]ettings", id="settings-btn")
                yield Button("🔄 [b][cyan]R[/cyan][/b]efresh", id="refresh-btn")
                yield Button("🚪 [b][cyan]Q[/cyan][/b]uit", id="quit-btn")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize application on mount."""
        self.title = "Terminal News Application v0.1.0"
        self._load_category(Category.US)
        # Set initial focus on first category button
        try:
            first_button = self.query("#categories-panel Button").first()
            if first_button:
                first_button.focus()
        except:
            pass
    
    def _load_category(self, category: Category) -> None:
        """Load articles for a category."""
        async def fetch():
            feeds = self.cfg.get_feeds_for_category(category.value)
            scraping = self.cfg.get_scraping_sources_for_category(category.value)
            
            # Try cache first
            cached = self.cache.get_articles(category=category, max_age_hours=6, limit=20)
            if cached:
                return cached
            
            # Fetch from sources
            articles = await self.handler.fetch_category(feeds, scraping, category, limit_per_source=5)
            if articles:
                self.cache.save_articles(articles)
            return articles
        
        # Run async fetch
        task = asyncio.create_task(fetch())
        self._update_display(task, category)
    
    def _update_display(self, task, category: Category) -> None:
        """Update display with fetched articles."""
        async def update():
            try:
                articles = await task
                self.articles = articles
                self.article_view_mode = "list"
                
                # Update UI with article list
                articles_panel = self.query_one("#articles-panel", ScrollableContainer)
                articles_panel.remove_children()
                
                # Add header
                header = Static(f"📂 {category.value.upper()} NEWS ({len(articles)} articles)\n")
                articles_panel.mount(header)
                
                if not articles:
                    articles_panel.mount(Static("No articles found. Check your connection or try another category."))
                else:
                    # Create clickable buttons for each article
                    for i, article in enumerate(articles[:15], 1):
                        headline = article.headline[:self.cfg.ui.max_headline_length]
                        source = article.source[:15]
                        btn = Button(f"{i}. {headline}\n   📍 {source}", id=f"article-{i-1}", classes="article-btn")
                        articles_panel.mount(btn)
            except Exception as e:
                articles_panel = self.query_one("#articles-panel", ScrollableContainer)
                articles_panel.remove_children()
                articles_panel.mount(Static(f"Error loading articles: {e}"))
        
        asyncio.create_task(update())
    
    def _show_article_detail(self, article: Article) -> None:
        """Show detail view of an article."""
        self.article_view_mode = "detail"
        self.selected_article = article
        
        articles_panel = self.query_one("#articles-panel", ScrollableContainer)
        articles_panel.remove_children()
        
        # Article detail view
        detail_content = f"""[b]{article.headline}[/b]

📍 Source: {article.source}
⏰ Published: {article.published_at or 'Unknown'}
✍️  Author: {article.author or 'Unknown'}
🏷️  Tags: {', '.join(article.tags) if article.tags else 'None'}

{'─' * 60}

{article.content or article.summary or 'No content available'}

{'─' * 60}

"""
        
        articles_panel.mount(Static(detail_content))
        
        # Display URL
        articles_panel.mount(Static(f"\n🔗 {article.url}\n"))
        
        articles_panel.mount(Static("\n[dim]Press ESC or Backspace to go back to the list[/dim]"))
    
    def action_quit(self) -> None:
        """Handle quit action."""
        self.exit()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle category button clicks."""
        button_id = event.button.id
        
        logger.info(f"Button pressed: {button_id}")
        
        if button_id == "settings-btn":
            self._show_settings()
        elif button_id == "refresh-btn":
            self._load_category(self.state.current_category)
        elif button_id == "quit-btn":
            self.exit()
        elif button_id and button_id.startswith("article-"):
            # Handle article click
            try:
                article_index = int(button_id.split("-")[1])
                if 0 <= article_index < len(self.articles):
                    self._show_article_detail(self.articles[article_index])
            except (ValueError, IndexError):
                pass
        else:
            category_map = {
                "cat-breaking": Category.BREAKING,
                "cat-agentic-dev": Category.AGENTIC_AI_DEV,
                "cat-agentic-bus": Category.AGENTIC_AI_BUS,
                "cat-us": Category.US,
                "cat-world": Category.WORLD,
                "cat-tech": Category.TECH,
                "cat-business": Category.BUSINESS,
                "cat-science": Category.SCIENCE,
            }
            if button_id in category_map:
                self._load_category(category_map[button_id])

    def on_key(self, event) -> None:
        """Handle keyboard shortcuts."""
        if event.key in ["escape", "backspace"]:
            # Go back from article detail to list
            if self.article_view_mode == "detail":
                self._load_category(self.state.current_category)
                return
        
        if event.key == "s":
            self._show_settings()
        elif event.key == "r":
            if self.current_view == "dashboard":
                self._load_category(self.state.current_category)
        elif event.key == "q":
            self.exit()
        elif event.key == "left":
            # Focus on categories panel
            try:
                categories = self.query("#categories-panel Button").first()
                if categories:
                    categories.focus()
            except:
                pass
        elif event.key == "right":
            # Focus on articles panel
            try:
                articles = self.query_one("#articles-panel")
                if articles:
                    articles.focus()
            except:
                pass
        elif event.key in ["up", "down"]:
            # Let Textual handle navigation between buttons
            pass
        elif self.current_view == "dashboard":
            key_map = {
                "1": Category.US,
                "2": Category.WORLD,
                "3": Category.TECH,
                "4": Category.BUSINESS,
                "5": Category.SCIENCE,
            }
            cat = key_map.get(event.key)
            if cat:
                self._load_category(cat)
    
    def _show_settings(self) -> None:
        """Show settings view."""
        self.current_view = "settings"
        main_container = self.query_one("#main-container", Container)
        main_container.remove_children()
        
        settings_view = SettingsView(self.cfg)
        main_container.mount(settings_view)
    
    def _show_dashboard(self) -> None:
        """Return to dashboard view."""
        self.current_view = "dashboard"
        main_container = self.query_one("#main-container", Container)
        main_container.remove_children()
        
        # Mount content_area first to the DOM
        content_area = Horizontal(id="content-area")
        main_container.mount(content_area)
        
        # Now mount children to content_area (which is now in the DOM)
        categories_panel = Vertical(id="categories-panel")
        content_area.mount(categories_panel)
        categories_panel.mount(Label("📂 Categories", id="categories-header"))
        categories_panel.mount(Button("🌟 Breaking News", id="cat-breaking"))
        categories_panel.mount(Button("🤖 Agentic AI Developer", id="cat-agentic-dev"))
        categories_panel.mount(Button("💼 Agentic AI Business", id="cat-agentic-bus"))
        categories_panel.mount(Button("🗽 US News", id="cat-us"))
        categories_panel.mount(Button("🌍 World", id="cat-world"))
        categories_panel.mount(Button("💻 Tech", id="cat-tech"))
        categories_panel.mount(Button("💼 Business", id="cat-business"))
        categories_panel.mount(Button("🔬 Science", id="cat-science"))
        
        # Right panel: Articles
        articles_panel = ScrollableContainer(id="articles-panel")
        content_area.mount(articles_panel)
        articles_panel.mount(Static("Select a category to view articles", id="articles-list"))
        
        # Bottom bar with controls - mount to main_container first, then add children
        bottom_bar = Horizontal(id="top-bar")
        main_container.mount(bottom_bar)
        bottom_bar.mount(Button("⚙️  [b][cyan]S[/cyan][/b]ettings", id="settings-btn"))
        bottom_bar.mount(Button("🔄 [b][cyan]R[/cyan][/b]efresh", id="refresh-btn"))
        bottom_bar.mount(Button("🚪 [b][cyan]Q[/cyan][/b]uit", id="quit-btn"))
        
        # Reload current category
        self._load_category(self.state.current_category)
    
    def on_back_to_dashboard_message(self, message: BackToDashboardMessage) -> None:
        """Handle BackToDashboardMessage from settings view."""
        self._show_dashboard()
    
    def action_settings(self) -> None:
        """Handle settings action."""
        self._show_settings()
    
    BINDINGS = []


def main():
    """Main entry point for the terminal news application."""
    app = NewsAppUI()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
