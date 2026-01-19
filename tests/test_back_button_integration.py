"""Integration tests for Settings back button functionality."""

import pytest
from unittest.mock import Mock
from textual.pilot import Pilot

from src.main import NewsAppUI
from src.ui.settings import BackToDashboardMessage, SettingsView
from src.config import ConfigManager


class TestBackButtonIntegration:
    """Test the complete back button flow in the app."""
    
    @pytest.mark.asyncio
    async def test_back_button_navigation_flow(self):
        """Test complete flow: Dashboard -> Settings -> Dashboard via back button."""
        app = NewsAppUI()
        
        async with app.run_test() as pilot:
            # Initial state: should be on dashboard
            assert app.current_view == "dashboard", "Should start on dashboard"
            
            # Open settings
            app._show_settings()
            await pilot.pause()
            assert app.current_view == "settings", "Should be on settings after _show_settings()"
            
            # Simulate back button press by posting message
            app.post_message(BackToDashboardMessage())
            await pilot.pause()
            
            # Should be back on dashboard
            assert app.current_view == "dashboard", "Should return to dashboard after back button"
    
    @pytest.mark.asyncio
    async def test_back_button_multiple_cycles(self):
        """Test multiple back-and-forth cycles work without errors."""
        app = NewsAppUI()
        
        async with app.run_test() as pilot:
            # Cycle 1
            app._show_settings()
            await pilot.pause()
            assert app.current_view == "settings"
            
            app.post_message(BackToDashboardMessage())
            await pilot.pause()
            assert app.current_view == "dashboard"
            
            # Cycle 2
            app._show_settings()
            await pilot.pause()
            assert app.current_view == "settings"
            
            app.post_message(BackToDashboardMessage())
            await pilot.pause()
            assert app.current_view == "dashboard"
            
            # Cycle 3
            app._show_settings()
            await pilot.pause()
            assert app.current_view == "settings"
            
            app.post_message(BackToDashboardMessage())
            await pilot.pause()
            assert app.current_view == "dashboard"
    
    @pytest.mark.asyncio
    async def test_back_to_dashboard_message_handler_exists_and_works(self):
        """Test that on_back_to_dashboard_message handler exists and handles message."""
        app = NewsAppUI()
        
        async with app.run_test() as pilot:
            # Verify handler exists
            assert hasattr(app, 'on_back_to_dashboard_message'), \
                "App must have on_back_to_dashboard_message handler"
            
            # Verify it's callable
            handler = getattr(app, 'on_back_to_dashboard_message')
            assert callable(handler), "on_back_to_dashboard_message must be callable"
            
            # Test the handler by switching to settings and posting message
            app._show_settings()
            await pilot.pause()
            
            # Create and post message
            message = BackToDashboardMessage()
            app.post_message(message)
            await pilot.pause()
            
            # Should return to dashboard
            assert app.current_view == "dashboard", \
                "Handler should return to dashboard"
    
    @pytest.mark.asyncio
    async def test_settings_view_button_posts_correct_message(self):
        """Test that Settings view back button posts BackToDashboardMessage."""
        config = ConfigManager()
        settings_view = SettingsView(config)
        
        # Mock post_message to capture what's posted
        settings_view.post_message = Mock()
        
        # Simulate back button press
        from textual.widgets import Button
        button_event = Mock(spec=Button.Pressed)
        button_event.button = Mock()
        button_event.button.id = "back-btn"
        
        # Call handler
        settings_view.on_button_pressed(button_event)
        
        # Verify BackToDashboardMessage was posted
        settings_view.post_message.assert_called_once()
        call_args = settings_view.post_message.call_args
        message = call_args[0][0]
        assert isinstance(message, BackToDashboardMessage), \
            f"Expected BackToDashboardMessage, got {type(message)}"
