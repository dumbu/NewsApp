# NewsApp Settings Feature

## Overview
Added a settings view where users can:
- View RSS feed URLs for each news category
- Edit existing feed URLs
- Add new custom feeds
- Save changes back to the configuration

## How to Use

### Access Settings
1. Run the app: `./newsapp`
2. Press **S** key or click the **⚙️ Settings** button
3. You'll see the Settings screen

### Settings Screen Features

**Category Selector**
- Dropdown menu to select which category's feeds to view/edit
- Default opens to "US" category

**Feed Management**
- Shows all RSS feeds assigned to the selected category
- Each feed displays:
  - Feed name (e.g., "techcrunch", "bbc_tech")
  - Current feed URL in an editable text field

**Actions**
- **✅ Save**: Saves all feed URL changes to config file
- **+ Add Feed**: Adds a new custom feed entry for the category
- **← Back**: Returns to the dashboard without saving

### Example Workflow

1. **View Tech Feeds**
   - Press S to open Settings
   - Select "tech" from Category dropdown
   - See all tech feeds (TechCrunch, GitHub Trending, Hacker News, etc.)

2. **Update a Feed URL**
   - Click on the URL field for any feed
   - Edit the URL to your preferred source
   - Click "✅ Save"

3. **Add Custom Feed**
   - Click "+ Add Feed"
   - A new entry "custom_1" is created with placeholder URL
   - Go back and edit the URL you want
   - Save

4. **Return to Dashboard**
   - Click "← Back" to return to news dashboard
   - Click a category button to load the updated feeds

## Technical Details

### New Files
- `src/ui/settings.py`: Settings view component with feed management

### Modified Files
- `src/main.py`: Added settings button, keyboard shortcut (S), and view switching
- `src/config/__init__.py`: Enhanced UIConfig with more settings fields

### Features
- Async configuration loading and saving
- Live feed editing without restarting app
- Category-based feed organization
- Persistent storage to YAML config file
- Error handling and logging

## Categories Supported
- US News
- World News
- Technology
- Business
- Science
- Sports (ESPN, BBC)
- Entertainment (BBC, etc.)

## Default Feeds
The app comes with pre-configured feeds for each category:

**Tech**: HackerNews, GitHub Trending, TechCrunch, Wired, BBC Tech
**US**: BBC US & Canada feed
**World**: BBC World feed  
**Business**: BBC Business feed
**Science**: ScienceDaily, Nature journal
**Sports**: BBC Sports
**Entertainment**: BBC Entertainment

## Configuration Storage
Settings are saved to: `config/config.yaml`

Format:
```yaml
news:
  rss_feeds:
    techcrunch:
      url: "https://techcrunch.com/feed/"
      categories: ["tech", "agentic_ai", "business"]
    ...
```

## Troubleshooting

### "No feeds configured for this category"
- The category might not have any feeds assigned
- Use "+ Add Feed" to add one
- Save and go back to dashboard

### Feed not updating after editing
- Make sure to click "✅ Save" 
- Check that the URL is valid and accessible
- Some feeds may require authentication or have CORS restrictions

### Changes not persisting
- Check file permissions on `config/config.yaml`
- Ensure the Docker volume is mounted correctly: `-v ./config:/app/config`
