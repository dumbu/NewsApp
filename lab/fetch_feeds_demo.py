#!/usr/bin/env python3
"""Demo script to fetch and display RSS feed content."""

import asyncio
import sys
import os
sys.path.insert(0, '/app/src')
os.chdir('/app')

from src.config import ConfigManager
from src.api import NewsHandler


async def main():
    """Fetch and display feeds for the new categories."""
    config = ConfigManager()
    handler = NewsHandler(config)
    
    categories = [
        ("breaking", "Breaking News"),
        ("agentic_ai_dev", "Agentic AI Developer"),
        ("agentic_ai_business", "Agentic AI Business"),
    ]
    
    for cat_id, cat_name in categories:
        print(f"\n{'='*80}")
        print(f"📰 {cat_name.upper()}")
        print(f"{'='*80}")
        
        feeds = config.get_feeds_for_category(cat_id)
        print(f"\nConfigured feeds: {len(feeds)}")
        for feed in feeds:
            print(f"  • {feed['name']}: {feed['url']}")
        
        print(f"\nFetching articles...")
        articles = await handler.fetch_category(cat_id, limit=5)
        
        if not articles:
            print("  ❌ No articles fetched")
            continue
        
        print(f"  ✅ Fetched {len(articles)} articles\n")
        
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article.headline[:75]}")
            print(f"   Source: {article.source}")
            print(f"   URL: {article.url}")
            if article.summary:
                summary_text = article.summary[:150].replace('\n', ' ')
                print(f"   Summary: {summary_text}...")
            if article.content:
                content_preview = article.content[:200].replace('\n', ' ')
                print(f"   Content: {content_preview}...")
            print()


if __name__ == "__main__":
    asyncio.run(main())
