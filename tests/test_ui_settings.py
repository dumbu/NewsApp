"""Tests for UI settings view."""

import pytest
from src.ui.settings import SettingsView
from src.models import Category


class TestSettingsView:
    """Tests for SettingsView."""
    
    def test_settings_view_initialization(self, config_manager):
        """Test SettingsView can be initialized."""
        settings = SettingsView(config_manager)
        assert settings is not None
        assert settings.config == config_manager
        assert settings.current_category == Category.US
    
    def test_settings_view_default_category(self, config_manager):
        """Test settings view starts with US category."""
        settings = SettingsView(config_manager)
        assert settings.current_category == Category.US
    
    def test_settings_view_feed_inputs(self, config_manager):
        """Test feed inputs dictionary is initialized."""
        settings = SettingsView(config_manager)
        assert isinstance(settings.feed_inputs, dict)
        assert len(settings.feed_inputs) == 0  # Empty until mounted
