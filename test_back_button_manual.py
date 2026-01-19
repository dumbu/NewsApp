#!/usr/bin/env python3
"""Manual test script to verify back button functionality in Settings."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import NewsAppUI
from src.ui.settings import BackToDashboardMessage, SettingsView
from src.config import ConfigManager


async def test_back_button_flow():
    """Test the complete back button flow: Dashboard -> Settings -> Dashboard."""
    print("🧪 Testing Back Button Flow")
    print("=" * 60)
    
    # Create app
    app = NewsAppUI()
    
    # Start app in a task
    app_task = asyncio.create_task(app.run_async())
    
    # Give app time to initialize
    await asyncio.sleep(2)
    
    try:
        # Verify we're on dashboard initially
        assert app.current_view == "dashboard", f"Expected dashboard, got {app.current_view}"
        print("✅ Step 1: Started on dashboard")
        
        # Open settings
        app._show_settings()
        await asyncio.sleep(0.5)
        assert app.current_view == "settings", f"Expected settings, got {app.current_view}"
        print("✅ Step 2: Opened Settings successfully")
        
        # Simulate back button press by posting message
        app.post_message(BackToDashboardMessage())
        await asyncio.sleep(0.5)
        
        # Verify we're back on dashboard
        assert app.current_view == "dashboard", f"Expected dashboard after back, got {app.current_view}"
        print("✅ Step 3: Back button returned to dashboard")
        
        # Test multiple back-and-forth
        app._show_settings()
        await asyncio.sleep(0.5)
        app.post_message(BackToDashboardMessage())
        await asyncio.sleep(0.5)
        assert app.current_view == "dashboard", "Failed after second cycle"
        print("✅ Step 4: Second cycle works (Settings -> Dashboard)")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Back button works correctly!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Exit app
        app.exit()
        try:
            await asyncio.wait_for(app_task, timeout=2)
        except asyncio.TimeoutError:
            print("⚠️  App didn't exit cleanly")


if __name__ == "__main__":
    asyncio.run(test_back_button_flow())
