"""Settings view for NewsApp - manage feed URLs."""

import logging
from typing import Dict, List

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button, Input, Label, Select
from textual.message import Message

from ..config import ConfigManager
from ..models import Category

logger = logging.getLogger(__name__)


class BackToDashboardMessage(Message):
    """Message to go back to dashboard."""
    pass


class SaveSettingsMessage(Message):
    """Message to save settings."""
    def __init__(self, feeds: Dict):
        super().__init__()
        self.feeds = feeds


class SettingsView(Static):
    """Settings panel for managing feed URLs."""
    
    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.feeds_container = None
        self.current_category = Category.US
        self.feed_inputs: Dict[str, Input] = {}
    
    def compose(self) -> ComposeResult:
        """Create settings UI."""
        with Container():
            with Vertical():
                yield Label("⚙️  Settings - Manage News Sources")
                yield Label("Select a category and edit RSS feed URLs:")
                
                # Category selector - using tuples of (label, value)
                categories = [(c.value.upper(), c.value) for c in Category]
                select_widget = Select(
                    options=categories,
                    prompt="Select Category",
                    id="category-select"
                )
                yield select_widget
                
                # Feeds list
                yield Label("Feed URLs for this category:")
                self.feeds_container = ScrollableContainer(id="feeds-container")
                yield self.feeds_container
                
                # Buttons
                with Horizontal():
                    yield Button("✅ Save", id="save-btn")
                    yield Button("+ Add Feed", id="add-feed-btn")
                    yield Button("← Back", id="back-btn")
    
    def on_mount(self) -> None:
        """Initialize settings view."""
        self._update_feeds_display()
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle category selection change."""
        try:
            self.current_category = Category(event.value)
            self._update_feeds_display()
        except Exception as e:
            logger.error(f"Error changing category: {e}")
    
    def _update_feeds_display(self) -> None:
        """Update feeds display for current category."""
        self.feed_inputs.clear()
        self.feeds_container.remove_children()
        
        feeds = self.config.get_feeds_for_category(self.current_category.value)
        
        if not feeds:
            self.feeds_container.mount(Label("No feeds configured for this category"))
            return
        
        for feed_info in feeds:
            feed_name = feed_info.get('name', 'Unknown')
            feed_url = feed_info.get('url', '')
            
            # Create label for feed name
            label = Label(f"📰 {feed_name}")
            self.feeds_container.mount(label)
            
            # Create input field for feed URL
            feed_input = Input(value=feed_url, id=f"feed-{feed_name}")
            self.feeds_container.mount(feed_input)
            self.feed_inputs[feed_name] = feed_input
            
            # Add spacer
            spacer = Static("", height=1)
            self.feeds_container.mount(spacer)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "back-btn":
            self.post_message(BackToDashboardMessage())
        
        elif button_id == "save-btn":
            self._save_feeds()
        
        elif button_id == "add-feed-btn":
            self._add_new_feed()
    
    def _save_feeds(self) -> None:
        """Save modified feed URLs back to config."""
        try:
            # Update the feeds in config
            for feed_name, feed_input in self.feed_inputs.items():
                new_url = feed_input.value
                
                # Find and update the feed in config
                if feed_name in self.config.news.rss_feeds:
                    self.config.news.rss_feeds[feed_name]['url'] = new_url
                    logger.info(f"Updated feed {feed_name}: {new_url}")
            
            # Save to YAML file
            self.config.save_config()
            logger.info("Settings saved successfully")
            
            # Show confirmation
            self.feeds_container.mount(Label("✅ Settings saved!"))
        
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            self.feeds_container.mount(Label(f"❌ Error saving: {e}"))
    
    def _add_new_feed(self) -> None:
        """Add a new feed for this category."""
        try:
            new_feed_name = f"custom_{len(self.feed_inputs) + 1}"
            new_feed_url = "https://example.com/feed.xml"
            
            # Add to config
            if new_feed_name not in self.config.news.rss_feeds:
                self.config.news.rss_feeds[new_feed_name] = {
                    "url": new_feed_url,
                    "categories": [self.current_category.value],
                }
                logger.info(f"Added new feed: {new_feed_name}")
            
            # Refresh display
            self._update_feeds_display()
        
        except Exception as e:
            logger.error(f"Error adding feed: {e}")
