"""Terminal News Application - Main Entry Point"""

import sys
import asyncio
import logging

from textual.app import ComposeResult, App
from textual.widgets import Header, Footer, Static, Button, Label
from textual.containers import Container, Vertical, Horizontal
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
    
    def __init__(self):
        super().__init__()
        self.cfg = ConfigManager()
        self.cache = CacheManager(db_path=self.cfg.cache.location)
        self.handler = NewsHandler()
        self.state = AppState()
        self.articles = []
        self.current_view = "dashboard"  # "dashboard" or "settings"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            with Vertical():
                yield Label("📰 Terminal News App")
                yield Label("Press 1-5 to select category, S for settings, Q to quit")
                
                with Horizontal():
                    yield Button("🇺🇸 US", id="cat-us")
                    yield Button("🌍 World", id="cat-world")
                    yield Button("💻 Tech", id="cat-tech")
                    yield Button("💼 Business", id="cat-business")
                    yield Button("🔬 Science", id="cat-science")
                
                with Horizontal():
                    yield Button("⚙️  Settings", id="settings-btn")
                    yield Button("🔄 Refresh", id="refresh-btn")
                
                yield Static("Loading...", id="articles-list")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize application on mount."""
        self.title = "Terminal News Application v0.1.0"
        self._load_category(Category.US)
    
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
                
                # Format articles for display
                content = f"\n📂 {category.value.upper()} NEWS ({len(articles)} articles)\n\n"
                if not articles:
                    content += "No articles found. Check your connection or try another category."
                else:
                    for i, article in enumerate(articles[:15], 1):
                        headline = article.headline[:self.cfg.ui.max_headline_length]
                        source = article.source[:15]
                        content += f"{i}. {headline}\n   📍 {source}\n\n"
                
                # Update UI
                articles_widget = self.query_one("#articles-list", Static)
                articles_widget.update(content)
            except Exception as e:
                articles_widget = self.query_one("#articles-list", Static)
                articles_widget.update(f"Error loading articles: {e}")
        
        asyncio.create_task(update())
    
    def action_quit(self) -> None:
        """Handle quit action."""
        self.exit()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle category button clicks."""
        button_id = event.button.id
        
        if button_id == "settings-btn":
            self._show_settings()
        elif button_id == "refresh-btn":
            self._load_category(self.state.current_category)
        else:
            category_map = {
                "cat-us": Category.US,
                "cat-world": Category.WORLD,
                "cat-tech": Category.TECH,
                "cat-business": Category.BUSINESS,
                "cat-science": Category.SCIENCE,
            }
            if button_id in category_map:
                self._load_category(category_map[button_id])
    
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
        
        # Rebuild dashboard UI
        with main_container:
            with Vertical():
                yield Label("📰 Terminal News App")
                yield Label("Press 1-5 to select category, S for settings, Q to quit")
                
                with Horizontal():
                    yield Button("🇺🇸 US", id="cat-us")
                    yield Button("🌍 World", id="cat-world")
                    yield Button("💻 Tech", id="cat-tech")
                    yield Button("💼 Business", id="cat-business")
                    yield Button("🔬 Science", id="cat-science")
                
                with Horizontal():
                    yield Button("⚙️  Settings", id="settings-btn")
                    yield Button("🔄 Refresh", id="refresh-btn")
                
                yield Static("Loading...", id="articles-list")
        
        # Reload current category
        self._load_category(self.state.current_category)
    
    def on_message(self, message: Message) -> None:
        """Handle app messages."""
        if isinstance(message, BackToDashboardMessage):
            self._show_dashboard()
    
    def action_settings(self) -> None:
        """Handle settings action."""
        self._show_settings()
    
    BINDINGS = [("q", "quit", "Quit"), ("s", "settings", "Settings")]


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
