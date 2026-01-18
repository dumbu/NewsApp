# NewsApp - Requirements Document

## Project Overview
A terminal-based news application that displays news headlines across various genres in an interactive, dashboard-style UI. The application fetches real-time news data and presents it in an organized manner for quick consumption.

## 1. Functional Requirements

### 1.1 News Categories
The application shall support the following news categories:
- **US News** - Domestic United States news
- **World News** - International news stories
- **Local News** - Regional/local news (configurable by user location)
- **Technology** - Tech industry news and product launches
- **Business** - Business, finance, and market news
- **Deals & Shopping** - Offers, discounts, and shopping deals
- **Sports** - Sports news and updates
- **Entertainment** - Movies, TV, celebrities, entertainment
- **Science & Health** - Scientific discoveries and health updates

**Industry News** (configurable, covers specialized sectors):
- **Manufacturing** - Industrial production, supply chain, manufacturing technology
- **Life Sciences** - Biotech, pharma, healthcare innovation, medical research
- **Automotive** - Car industry, EVs, autonomous vehicles, mobility solutions
- **Aviation** - Airlines, aerospace, aircraft technology, aviation industry
- **E-Commerce & Retail** - Online retail, shopping platforms, retail technology

**Emerging Technology**:
- **Agentic AI** - AI agents, autonomous AI systems, agent-based intelligence, AI automation

### 1.2 Dashboard Display
- Display headlines from multiple categories simultaneously
- Show article title, source, and publication time
- Display category indicators/colors for visual distinction
- Implement scrolling through news items within each category
- Support pagination or continuous loading of more articles
- Real-time or periodic refresh of news data

### 1.3 News Data Sources

#### Primary Methods (No API Key Required)
1. **RSS/Atom Feeds** from trusted news sources:
   - Major publishers: BBC, Reuters, Associated Press, NPR, etc.
   - Technology: TechCrunch, Wired, The Verge, etc.
   - Business: Bloomberg, Financial Times, CNBC, etc.
   - Local: NPR local feeds, state-specific news outlets
   - Sports: ESPN, Sports Illustrated, BBC Sports
   - Entertainment: Variety, The Hollywood Reporter, Deadline
   - Science: Nature, Science Magazine, Scientific American
   - Manufacturing: Industry Week, Control Engineering, etc.
   - Life Sciences: BiopharmGuy, STAT News, endpoints News, etc.
   - Automotive: Automotive News, Car and Driver, Motor Trend, etc.
   - Aviation: Aviation Week, FlightGlobal, AirGuide, etc.
   - E-Commerce/Retail: Retail Dive, eWEEK, Internet Retailer, etc.
   - Agentic AI: ArXiv AI, AI News, DeepLearning.AI, etc.

2. **Web Scraping** (with respect to robots.txt):
   - Scrape headlines from trusted news websites
   - Parse article metadata (title, description, image, author)
   - Respect rate limiting and robots.txt
   - Support for websites without RSS feeds

#### Optional: API Integration (with API Key)
- NewsAPI integration (optional, configurable)
- Support multiple API providers as fallback
- Graceful degradation if API unavailable

#### General Requirements
- Support configurable news sources
- Handle rate limiting gracefully
- Cache news data locally to reduce requests
- Implement error handling for feed/scraping failures
- Verify source authenticity before display
- Support adding custom RSS feeds
- Parse metadata: title, description, image, publication date, source

### 1.4 User Interaction

#### Primary Navigation
- Navigate between categories using keyboard/arrow keys
- Navigate between headlines within a category (up/down)
- Toggle categories on/off
- Search/filter by keyword
- Sort by recency, relevance, or popularity
- Customizable refresh interval

#### Drill-Down / Detail View (Key Feature)
**Clickable Headlines with In-Depth Information:**
- Press Enter on a headline to enter "drill-down" view
- Display full article details:
  - Complete headline and subheading
  - Full article description/summary
  - Article image/thumbnail
  - Source attribution with publication date
  - Author name (if available)
  - Article URL
  - Word count and estimated read time
  - Category tags
  - Related stories (if available)
- Show related articles from the same source or category
- Display article content preview (first 300-500 characters)
- Option to open full article in browser
- Navigate between related articles within drill-down view
- "Back" option to return to category headline list
- Keyboard shortcuts:
  - `Enter` - View detailed article
  - `o` - Open in browser
  - `r` - Show related articles
  - `b` - Go back to category view
  - `n`/`p` - Next/previous related article

### 1.5 User Preferences
- Save user's preferred categories
- Save user's location (for local news)
- Store API configuration
- Remember last viewed position
- Dark mode / light mode support (if applicable to terminal)

## 2. Non-Functional Requirements

### 2.1 Performance
- Application start-up time < 2 seconds
- News refresh time < 5 seconds per category
- Memory footprint < 100MB
- Support at least 50-100 headlines per category simultaneously

### 2.2 Reliability
- Graceful handling of network failures
- Fallback to cached data if API unavailable
- Error messages displayed to user without crashing
- Automatic retry logic for failed requests

### 2.3 Scalability
- Support adding new news sources easily
- Support adding new categories without code changes
- Configuration-driven architecture

### 2.4 Security
- Secure storage of API keys (environment variables, config files)
- No credential logging
- HTTPS/TLS for all API calls
- Validate and sanitize all external data

### 2.5 Maintainability
- Well-documented code
- Modular architecture
- Comprehensive logging
- Unit and integration tests

## 3. Technical Architecture

### 3.1 Technology Stack
- **Language**: Python 3.11+
- **Terminal UI Library**: Textual (modern, async-friendly, fully Python)
- **HTTP Client**: aiohttp (async, fully Python)
- **RSS Parsing**: feedparser (for RSS/Atom feeds)
- **Web Scraping**: BeautifulSoup4 + aiohttp (for trusted news sources)
- **Data Format**: JSON, XML
- **Database**: SQLite (for local caching, file-based)
- **Testing**: pytest, pytest-asyncio
- **Package Manager**: pip with requirements.txt
- **Containerization**: Docker with Python virtual environment
- **Environment Management**: Python venv (built-in)

### 3.2 System Components

#### Core Modules
1. **News API Handler** - Fetch news from external APIs
2. **Data Models** - Article, Category, Source data structures
3. **UI Renderer** - Terminal UI with:
   - Dashboard view (headline list)
   - Detail view (drill-down modal/screen)
   - Related articles view
4. **Cache Manager** - Local storage and retrieval of articles
5. **Configuration Manager** - Handle user preferences and settings
6. **Error Handler** - Centralized error handling and logging
7. **Article Processor** - Extract and process article details for drill-down
8. **Related Articles Engine** - Find and display related articles
   - Based on same source
   - Based on similar categories
   - Based on keyword matching
   - Time-based relevance

#### Integration Points
- News API (primary data source)
- Local SQLite database (caching)
- Configuration files (JSON or YAML)
- Terminal interface (user interaction)

### 3.3 Data Flow
```
User Input (Dashboard) → UI Handler
        ↓
    Browse Headlines
        ↓
    Select Headline (Enter)
        ↓
    UI Renderer → Detail/Drill-Down View
        ↓
    Display Full Article + Related Articles
        ↓
    Article Processor:
      - Extract full content
      - Find related articles
      - Calculate read time
        ↓
    Cache Layer ← Article Data
        ↓
    Database Storage
        ↓
    User Navigation:
      - View related articles
      - Open in browser
      - Return to category (back button)
```

## 4. UI/UX Requirements

### 4.1 Layout

**Main Dashboard View:**
- Multi-column or tabbed layout showing different categories
- Category headers clearly visible
- Article count per category displayed
- Status bar showing last update time and loading status
- Help menu accessible with keyboard shortcut
- Highlight current/selected headline

**Detail/Drill-Down View:**
- Full-screen or modal display of article details
- Article content preview with scrolling
- Metadata panel (source, date, author, read time)
- Related articles section
- Navigation breadcrumb showing current position
- "Back to category" indicator

### 4.2 Navigation

**Dashboard Navigation:**
- Arrow keys / Vi keybindings for navigation between headlines
- Tab / Shift+Tab to switch between categories
- Enter to view full article details (drill-down)
- 'q' or Ctrl+C to quit gracefully
- '?' - Show help menu
- Configurable key bindings

**Detail View Navigation:**
- `o` - Open article in browser
- `r` - Show related articles
- `b` or `Esc` - Back to category view
- `n`/`p` - Navigate next/previous related article
- Up/Down - Scroll article content
- Space - Page down

### 4.3 Visual Design
- Clear visual separation between categories in main view
- Color coding by category (if terminal supports colors)
- Highlight current/selected item
- Truncate long headlines appropriately in list view
- Display read/unread status (optional)
- Visual distinction for drill-down view (modal or alternate screen)
- Clear indication of related articles section

## 5. Configuration Requirements

### 5.1 Configuration File (config.yaml or .env)
```yaml
# News source configuration
news_sources:
  # Primary method: RSS feeds (no API key required)
  rss_feeds:
    enabled: true
    sources:
      us:
        - name: "Reuters US"
          url: "https://feeds.reuters.com/reuters/businessNews"
        - name: "AP News"
          url: "https://apnews.com/apf/feeds/rss.xml"
      world:
        - name: "BBC World"
          url: "http://feeds.bbc.co.uk/news/world/rss.xml"
      tech:
        - name: "TechCrunch"
          url: "http://feeds.feedburner.com/TechCrunch"
      manufacturing:
        - name: "Industry Week"
          url: "https://www.industryweek.com/feed"
      lifesciences:
        - name: "STAT News"
          url: "https://www.statnews.com/feed"
      automotive:
        - name: "Automotive News"
          url: "https://www.autonews.com/feed"
      aviation:
        - name: "Aviation Week"
          url: "https://aviationweek.com/feed"
      ecommerce:
        - name: "Retail Dive"
          url: "https://www.retaildive.com/feed"
      agentic_ai:
        - name: "AI News"
          url: "https://www.artificialintelligence-news.com/feed"
      # ... more RSS feeds
  
  # Secondary method: Web scraping (no API key required)
  scraping:
    enabled: true
    sources:
      - name: "HackerNews"
        url: "https://news.ycombinator.com"
        selectors:
          title: ".titleline > a"
          link: ".titleline > a"
          score: ".score"
  
  # Optional: API-based sources (requires API key)
  api:
    enabled: false  # Set to true if using API
    provider: "newsapi"  # or alternative
    key: "YOUR_API_KEY"  # Only if enabled
    base_url: "https://newsapi.org/v2"
    request_timeout: 10

categories:
  enabled: [
    "us", "world", "tech", "business", "deals", "sports",
    "entertainment", "science", "local",
    "manufacturing", "lifesciences", "automotive", "aviation", "ecommerce",
    "agentic_ai"
  ]
  refresh_interval: 300  # seconds

ui:
  theme: "dark"
  color_mode: true
  columns: 2

cache:
  enabled: true
  ttl: 3600  # seconds
  db_path: "~/.newsapp/cache.db"
  # Scraping specific cache
  scrape_cache_ttl: 1800  # Shorter TTL for scraping

user:
  location: "US"
  language: "en"

rate_limiting:
  # Respect rate limits
  rss_request_delay: 1  # seconds between requests
  scraping_request_delay: 2  # seconds between scraping requests
  max_requests_per_hour: 100
```

### 5.2 News Source Configuration
- Support multiple RSS feed sources per category
- Configurable scraping targets with CSS selectors
- Optional API key support for fallback
- Add custom RSS feeds easily
- Verify source authenticity before parsing
- Request timeout settings
- Rate limiting to respect server resources

## 6. Deployment & Distribution

### 6.1 Docker Containerization
**Primary Deployment Method**: Docker with isolated Python virtual environment

#### Docker Requirements
- **Base Image**: python:3.11-slim-bullseye (lightweight, minimal footprint)
- **Virtual Environment**: Python venv created inside container at `/app/venv`
- **Workdir**: `/app` for application code
- **Volumes**:
  - `/app/.newsapp` - Persistent storage for cache, logs, and user config
  - `/app/config` - Configuration files (mounted from host)
  - `/app/logs` - Application logs
- **Entry Point**: Shell script to activate venv and run application
- **Port Exposure**: Not required (terminal-based app, runs interactively)
- **Environment Variables**:
  - `PYTHONUNBUFFERED=1` - Disable Python buffering for real-time logs
  - `PYTHONDONTWRITEBYTECODE=1` - Don't create .pyc files
  - `NEWS_API_KEY` - (Optional) News API key if using API-based sources
  - `CONFIG_PATH` - Path to config file (default: `/app/config/config.yaml`)
  - `USE_RSS_ONLY` - If set to true, only use RSS feeds (no scraping)

#### Docker Compose Setup
- Orchestrate container with volume mounts
- Environment variable configuration
- Easy start/stop/restart
- Support for interactive terminal mode (`docker-compose run -it`)

### 6.2 Installation Methods

#### Method 1: Docker (Recommended)
```bash
# Build image
docker build -t terminal-news-app:latest .

# Run with interactive terminal
docker run -it \
  -v ~/.newsapp:/app/.newsapp \
  -v ./config:/app/config \
  -e NEWS_API_KEY=your_api_key \
  terminal-news-app:latest

# Or use docker-compose
docker-compose up -it
```

#### Method 2: Local Development (Python venv)
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m src.main
```

#### Method 3: PyPI Package (Future)
- PyPI package (pip install terminal-news-app)
- Standalone executable via PyInstaller

### 6.3 Development
- GitHub repository with proper documentation
- CI/CD pipeline (GitHub Actions)
  - Automated testing on push
  - Docker image build and registry push
  - Python linting and type checking
- Version management with semantic versioning

### 6.4 Virtual Environment Management
- **Inside Docker**: Venv located at `/app/venv` with all dependencies installed during build
- **Local Development**: Create venv in project root: `python3.11 -m venv venv`
- **Dependency Management**: requirements.txt for reproducible builds
- **Activation Script**: Entry point automatically activates venv before running application

## 7. Testing Requirements

### 7.1 Unit Tests
- Test each module independently
- Mock external API calls
- Test cache layer operations
- Test data model validations

### 7.2 Integration Tests
- Test end-to-end workflows
- Test API integration with caching
- Test configuration loading
- Test UI interactions

### 7.3 Test Coverage
- Minimum 70% code coverage
- All error paths tested
- Edge cases covered

## 8. Future Enhancements

### Phase 2 Features
- Bookmark/save articles for later
- Article summary generation
- Personalized news feeds based on history
- Multi-language support
- Custom RSS feed sources
- News source filtering
- Trending stories tracking
- Article sentiment analysis
- Integration with note-taking apps

### Phase 3 Features
- Mobile companion app
- Email digest of top stories
- AI-powered news recommendations
- Voice-based news reading
- Offline reading mode with sync

## 9. Documentation

### 9.1 Required Documentation
- README.md - Project overview and quick start
- INSTALLATION.md - Detailed installation instructions (Docker, venv, PyPI)
- DOCKER.md - Docker-specific setup and usage guide
- CONFIGURATION.md - Configuration guide
- API_INTEGRATION.md - How to integrate new news sources
- DEVELOPMENT.md - Contribution guidelines and local development setup
- ARCHITECTURE.md - System design and architecture
- CHANGELOG.md - Version history
- Dockerfile - Docker image specification with venv setup
- docker-compose.yml - Docker Compose orchestration

### 9.2 Code Documentation
- Docstrings for all classes and functions
- Inline comments for complex logic
- Type hints throughout codebase

## 10. Success Criteria

### Core Features
- [ ] Application loads and displays headlines within 2 seconds (no API key required)
- [ ] All 15 news categories display headlines correctly from RSS/scraping sources
  - Core: US, World, Local, Tech, Business, Deals, Sports, Entertainment, Science
  - Industry: Manufacturing, Life Sciences, Automotive, Aviation, E-Commerce
  - Emerging: Agentic AI
- [ ] User can navigate between categories smoothly
- [ ] RSS feed parsing works for all configured sources
- [ ] Web scraping works for configured sites (respects robots.txt)

### Drill-Down Feature (Key Requirement)
- [ ] Headlines are clickable (Enter key activates)
- [ ] Drill-down view displays full article details:
  - Complete headline and description
  - Article image/thumbnail
  - Source, author, and publication date
  - Estimated read time
  - Full article preview
- [ ] Related articles display in drill-down view
- [ ] Can navigate between related articles
- [ ] "Open in browser" functionality works from drill-down view
- [ ] Back button returns to category headline list
- [ ] Keyboard shortcuts work correctly (o, r, b, n, p)

### Reliability & Quality
- [ ] Application handles feed/scraping failures gracefully
- [ ] Cached data persists across sessions
- [ ] 70%+ unit test coverage
- [ ] Zero security vulnerabilities in dependencies
- [ ] No external API keys required for basic functionality
- [ ] Respects rate limiting and robots.txt
- [ ] Application runs on macOS, Linux, and Windows

---

**Document Version**: 1.3  
**Last Updated**: January 15, 2026  
**Status**: Draft  
**Deployment**: Docker + Python venv (primary), Local venv (development), PyPI (future)  
**News Sources**: RSS Feeds + Web Scraping (primary, no API key required), NewsAPI (optional)  
**Key Feature**: Drill-down headline interaction with related articles
