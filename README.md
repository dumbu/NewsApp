# Terminal News Application

A fast, keyboard-driven terminal-based news application that displays headlines across multiple categories (US, World, Tech, Business, Deals, Sports, Entertainment, Science, Local) in a beautiful dashboard UI.

**🎉 No API Key Required!** Uses RSS feeds and web scraping from trusted news sources.

## Quick Links

- 📖 **[Full Documentation](docs/README.md)** - Complete user guide and features
- 📋 **[Requirements](docs/REQUIREMENTS.md)** - Project requirements and specifications
- 🐳 **[Docker Setup](docs/DOCKER.md)** - Docker and containerization guide
- 🤝 **[Contributing](docs/CONTRIBUTING.md)** - How to contribute to the project
- 📝 **[Changelog](docs/CHANGELOG.md)** - Version history and changes

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

### Docker (Recommended)

```bash
# Clone or download the repository
git clone <repo-url>
cd terminal-news-app

# Run with docker-compose
docker-compose up -it
```

### Local Installation

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.main
```

## Requirements

- Python 3.11+
- Internet connection (for fetching news)
- Terminal with color support (recommended)
- **No API key required!** Works out-of-the-box with RSS feeds

## Project Structure

```
.
├── src/                    # Application source code
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation (markdown files)
├── config/                 # Configuration templates
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # This file
```

## Documentation

For detailed information, see:

- [Full User Guide](docs/README.md) - Features, usage, and configuration
- [Requirements Document](docs/REQUIREMENTS.md) - Complete project specifications
- [Docker Guide](docs/DOCKER.md) - How to run in Docker containers
- [Contributing Guide](docs/CONTRIBUTING.md) - How to contribute
- [Changelog](docs/CHANGELOG.md) - Version history

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Status**: Early Development (v0.1.0)  
**Last Updated**: January 15, 2026
