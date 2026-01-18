"""Tests to verify the Settings back button fix."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.ui.settings import BackToDashboardMessage


class TestBackButtonFix:
    """Tests for the back button fix in Settings."""
    
    def test_back_to_dashboard_message_handler_exists(self):
        """Test that the message handler method exists in NewsAppUI."""
        # Import here to avoid dependency issues in test discovery
        from src.main import NewsAppUI
        
        # Verify the handler exists
        assert hasattr(NewsAppUI, 'on_back_to_dashboard_message'), \
            "NewsAppUI must have on_back_to_dashboard_message method"
        
        # Verify it's callable
        handler = getattr(NewsAppUI, 'on_back_to_dashboard_message')
        assert callable(handler), \
            "on_back_to_dashboard_message must be a callable method"
    
    def test_back_button_posts_message(self, config_manager):
        """Test that clicking back button posts BackToDashboardMessage."""
        from src.ui.settings import SettingsView
        from textual.widgets import Button
        
        # Create a settings view
        settings_view = SettingsView(config_manager)
        
        # Mock the post_message method
        settings_view.post_message = Mock()
        
        # Simulate back button press
        button_event = Mock(spec=Button.Pressed)
        button_event.button = Mock()
        button_event.button.id = "back-btn"
        
        # Call the button handler
        settings_view.on_button_pressed(button_event)
        
        # Verify message was posted
        settings_view.post_message.assert_called_once()
        
        # Verify it's the correct message type
        call_args = settings_view.post_message.call_args
        message = call_args[0][0]
        assert isinstance(message, BackToDashboardMessage), \
            f"Expected BackToDashboardMessage, got {type(message)}"
    
    def test_message_handler_signature(self):
        """Test that the message handler has the correct signature."""
        from src.main import NewsAppUI
        import inspect
        
        # Get the handler method
        handler = getattr(NewsAppUI, 'on_back_to_dashboard_message')
        
        # Check the signature
        sig = inspect.signature(handler)
        params = list(sig.parameters.keys())
        
        # Should have 'self' and 'message' parameters
        assert len(params) == 2, \
            f"Handler should have 2 parameters (self, message), got {len(params)}: {params}"
        assert params[0] == 'self', "First parameter should be 'self'"
        assert params[1] == 'message', "Second parameter should be 'message'"
        
        # Verify the message type annotation
        message_param = sig.parameters['message']
        assert message_param.annotation == BackToDashboardMessage, \
            f"Message parameter should be annotated as BackToDashboardMessage"
    
    @patch('src.main.NewsAppUI._show_dashboard')
    def test_message_handler_calls_show_dashboard(self, mock_show_dashboard):
        """Test that the message handler calls _show_dashboard."""
        from src.main import NewsAppUI
        
        # Create a mock app instance
        app = Mock(spec=NewsAppUI)
        app._show_dashboard = mock_show_dashboard
        
        # Get the handler and call it with app instance
        handler = NewsAppUI.on_back_to_dashboard_message
        message = BackToDashboardMessage()
        
        # Call the handler
        handler(app, message)
        
        # Verify _show_dashboard was called
        mock_show_dashboard.assert_called_once()
