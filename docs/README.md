# NewsApp

A fast, keyboard-driven terminal-based news application that displays headlines across multiple categories (US, World, Tech, Business, Deals, Sports, Entertainment, Science, Local) in a beautiful dashboard UI.

**🎉 No API Key Required!** Uses RSS feeds and web scraping from trusted news sources.

## Features

- 📰 **Multi-Category News** - US, World, Tech, Business, Deals, Sports, Entertainment, Science, Local
- 🔓 **No API Key Required** - Uses RSS feeds and web scraping from trusted sources
- ⌨️ **Keyboard Navigation** - Efficient navigation using arrow keys and vim keybindings
- 🔄 **Auto-Refresh** - Configurable automatic news refresh
- 💾 **Smart Caching** - Local caching to reduce network requests and support offline reading
- 🎨 **Beautiful Terminal UI** - Clean, organized dashboard layout
- 🔗 **Quick Access** - Open articles directly in your browser
- 📡 **Multiple Sources** - RSS feeds from major publishers (BBC, Reuters, AP, TechCrunch, etc.)
- 🕷️ **Web Scraping** - Supplement with scraping from trusted sites (respects robots.txt)
- 🔒 **Secure** - No credentials needed, respects rate limits

## Quick Start

### Installation

```bash
pip install newsapp
```

### First Run

```bash
# Simply run the application - no API key configuration needed!
newsapp
```

## Usage

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` | Navigate news items |
| `←/→` | Switch between categories |
| `Tab` | Next category |
| `Shift+Tab` | Previous category |
| `Enter` | Open article in browser |
| `r` | Refresh news |
| `s` | Search articles |
| `?` | Show help menu |
| `q` / `Ctrl+C` | Quit application |

## Configuration

Create a `config.yaml` file in `~/.newsapp/` to customize news sources:

```yaml
# News sources - RSS feeds are enabled by default
news_sources:
  rss_feeds:
    enabled: true
    # Pre-configured sources include BBC, Reuters, AP, TechCrunch, etc.
  
  scraping:
    enabled: true
    # Trusted scraping sources are pre-configured
  
  # Optional: Add your own News API key for additional coverage
  api:
    enabled: false  # Set to true only if you have an API key
    # key: "YOUR_API_KEY_HERE"

categories:
  enabled: ["us", "world", "tech", "business", "deals", "sports", "entertainment", "science"]
  refresh_interval: 300  # seconds

ui:
  theme: "dark"
  columns: 2
```

## Requirements

- Python 3.11+
- Internet connection (for fetching news)
- Terminal with color support (recommended)
- **No API key required!** Works out-of-the-box with RSS feeds

## Optional: Adding an API Key

To use additional news sources via NewsAPI:

1. Visit [https://newsapi.org](https://newsapi.org)
2. Sign up for a free account
3. Copy your API key
4. Add it to your `config.yaml` with `api.enabled: true`

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── ui/                  # Terminal UI components
│   ├── api/                 # News API integration
│   ├── models/              # Data models
│   ├── cache/               # Caching layer
│   └── config/              # Configuration management
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── config/                  # Configuration templates
├── REQUIREMENTS.md          # Project requirements
├── setup.py                 # Package setup
└── README.md                # This file
```

## Development

### Setup Development Environment

```bash
git clone <repo-url>
cd terminal-news-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Building Documentation

```bash
cd docs/
make html
```

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Roadmap

- [ ] Phase 1: Core functionality with multi-category display
- [ ] Phase 2: Bookmarks, personalization, custom feeds
- [ ] Phase 3: Mobile app, email digests, advanced analytics

## Troubleshooting

### No RSS feeds loading
- Check your internet connection
- Verify feed URLs are accessible
- Check logs in `~/.newsapp/logs/`

### Display Issues
- Ensure your terminal supports 256 colors: `echo $TERM`
- Try setting `TERM=xterm-256color` if colors aren't displaying

### Network Issues
- Check your internet connection
- Verify firewall settings
- The app respects rate limits - if you get rate-limited, it will use cached data

### API Key Issues (if using optional API)
- Ensure your API key is correctly set in the configuration
- Check that your API plan allows the number of requests
- The app works fine without an API key - it uses RSS feeds

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Status**: Early Development (v0.1.0)  
**Last Updated**: January 15, 2026
