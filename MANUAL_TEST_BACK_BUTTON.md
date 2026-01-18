# Manual Test Plan for Settings Back Button Fix

## Issue
The back button (← Back) in the Settings screen was not working - clicking it did nothing.

## Root Cause
The message handler in `NewsAppUI` was using a generic `on_message` method with type checking instead of following Textual's naming convention for message handlers.

## Fix
Changed the message handler from:
```python
def on_message(self, message: Message) -> None:
    if isinstance(message, BackToDashboardMessage):
        self._show_dashboard()
```

To:
```python
def on_back_to_dashboard_message(self, message: BackToDashboardMessage) -> None:
    """Handle BackToDashboardMessage from settings view."""
    self._show_dashboard()
```

## How to Test Manually

### Prerequisites
- Docker installed
- Repository cloned

### Test Steps

1. **Build and run the application:**
   ```bash
   docker compose up --build
   ```

2. **Access Settings screen:**
   - Once the app starts, press the `S` key OR click the "⚙️ Settings" button at the bottom
   - You should see the Settings screen with:
     - Category selector dropdown
     - List of RSS feeds for the selected category
     - Three buttons at the bottom: "✅ Save", "+ Add Feed", "← Back"

3. **Test Back Button:**
   - Click the "← Back" button
   - **Expected Result:** The app should return to the main dashboard view
   - **Previous Bug:** Button did nothing when clicked

4. **Test Settings Keyboard Shortcut:**
   - From the dashboard, press `S` to open Settings again
   - Click "← Back" to return
   - Verify you're back on the dashboard

5. **Test Settings Button:**
   - Click the "⚙️ Settings" button at the bottom
   - Verify Settings screen opens
   - Click "← Back"
   - Verify you return to dashboard

### Expected Behavior After Fix
- ✅ Clicking "← Back" in Settings returns to dashboard
- ✅ Dashboard is restored with categories panel and articles panel
- ✅ No errors in the logs
- ✅ Can navigate back and forth between Settings and Dashboard multiple times

### Additional Verification
- Test that other Settings buttons still work:
  - "✅ Save" saves changes
  - "+ Add Feed" adds a new feed
- Test that navigation with ESC key still works in article detail view

## Testing in Docker

```bash
# Clean build and run
docker compose down
docker compose build --no-cache
docker compose up

# Run tests (if test environment is available)
./newsapp test
```

## Code Changes Summary

**File:** `src/main.py`
**Lines:** 364-366
**Change:** Renamed message handler to follow Textual's `on_<message_name>` pattern

This fix aligns with Textual's message routing system, which automatically calls `on_<message_class_name_in_snake_case>` when a message of that type is posted.
