"""Manual test script to reproduce reported bugs."""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.DEBUG)

from src.config import ConfigManager
from src.cache import CacheManager
from src.api import NewsHandler
from src.models import Category

async def test_real_app_flow():
    """Test the actual app workflow."""
    print("=" * 60)
    print("Testing NewsApp Components")
    print("=" * 60)
    
    # Test 1: Config
    print("\n[1/5] Testing Config...")
    try:
        cfg = ConfigManager()
        print(f"✓ Config loaded")
        print(f"  - UI theme: {cfg.ui.theme}")
        print(f"  - Cache location: {cfg.cache.location}")
    except Exception as e:
        print(f"✗ Config failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Cache
    print("\n[2/5] Testing Cache...")
    try:
        cache = CacheManager(db_path=cfg.cache.location)
        print(f"✓ Cache initialized at {cfg.cache.location}")
        print(f"  - Database exists: {Path(cfg.cache.location).exists()}")
    except Exception as e:
        print(f"✗ Cache failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Fetch news for each category
    print("\n[3/5] Testing News Fetching...")
    handler = NewsHandler()
    
    for category in [Category.BREAKING, Category.AGENTIC_AI_DEV, Category.AGENTIC_AI_BUS, Category.US, Category.TECH]:
        print(f"\n  Category: {category.value}")
        try:
            feeds = cfg.get_feeds_for_category(category.value)
            scraping = cfg.get_scraping_sources_for_category(category.value)
            print(f"    - Feeds: {len(feeds)}")
            print(f"    - Scraping sources: {len(scraping)}")
            
            if not feeds and not scraping:
                print(f"    ⚠ No sources configured for {category.value}")
                continue
            
            articles = await handler.fetch_category(feeds, scraping, category, limit_per_source=3)
            print(f"    ✓ Fetched {len(articles)} articles")
            
            if articles:
                # Show first article
                print(f"    First: {articles[0].headline[:60]}...")
                
                # Try to cache
                cache.save_articles(articles)
                print(f"    ✓ Saved to cache")
                
                # Try to retrieve
                cached = cache.get_articles(category=category, max_age_hours=1, limit=5)
                print(f"    ✓ Retrieved {len(cached)} from cache")
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Test 4: Settings View
    print("\n[4/5] Testing Settings View...")
    try:
        from src.ui.settings import SettingsView
        settings = SettingsView(cfg)
        print(f"✓ Settings view created")
        print(f"  - Current category: {settings.current_category}")
        print(f"  - Feed inputs: {len(settings.feed_inputs)}")
    except Exception as e:
        print(f"✗ Settings view failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 5: Main App
    print("\n[5/5] Testing Main App...")
    try:
        from src.main import NewsAppUI
        app = NewsAppUI()
        print(f"✓ Main app created")
        print(f"  - Title: {app.TITLE}")
        print(f"  - Current category: {app.state.current_category}")
        # Don't actually run it
    except Exception as e:
        print(f"✗ Main app failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_real_app_flow())
