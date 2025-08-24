# Feature Plan: Extremely Simple Web UI Interface for Equipment Search

## Context
The user wants to create an extremely simple Web UI interface to search for items in the equipment database. This will provide a basic web-based way to search and view equipment without the complexity of the Slack integration.

## Technical Requirements
- Create a minimal web interface for searching equipment in the database
- Implement basic search functionality across equipment names and descriptions
- Display search results in a simple, readable format
- Keep the implementation extremely simple and lightweight

## Files to Create/Modify

### New Files
1. **`src/web/__init__.py`** - Web package initialization
2. **`src/web/app.py`** - Main Flask application with search endpoints
3. **`src/web/templates/search.html`** - Simple HTML template for search interface
4. **`src/web/static/style.css`** - Basic CSS styling
5. **`web_server.py`** - Entry point script to run the web server

### Modified Files
1. **`requirements.txt`** - Add Flask dependency
2. **`README.md`** - Add web UI usage instructions

## Implementation Details

### Phase 1: Data Layer (No changes needed)
- Existing Equipment model already has `search_equipment(query: str)` method
- Existing Category model already has `search_categories(query: str)` method
- Database connection infrastructure is already in place

### Phase 2: Web Interface
- **Flask Application (`src/web/app.py`)**:
  - Single route `/` for search form and results
  - Search endpoint that calls existing Equipment.search_equipment() method
  - Simple JSON response or rendered HTML with results
  
- **HTML Template (`src/web/templates/search.html`)**:
  - Single search input field
  - Search button
  - Results display area
  - Minimal styling with basic responsive design
  
- **CSS Styling (`src/web/static/style.css`)**:
  - Clean, simple design
  - Basic responsive layout
  - Equipment card styling for results

### Phase 3: Integration
- **Entry Point (`web_server.py`)**:
  - Simple script to run Flask development server
  - Database connection initialization
  - Basic error handling

## Search Algorithm
The existing `Equipment.search_equipment(query: str)` method already implements:
1. Full-text search across equipment name and description using PostgreSQL's `to_tsvector` and `plainto_tsquery`
2. Results ranked by relevance using `ts_rank`
3. Ordered by rank (descending) then by name

## Dependencies to Add
- **Flask==3.0.0** - Minimal web framework for the interface

## File Structure
```
src/
├── web/
│   ├── __init__.py
│   ├── app.py
│   ├── templates/
│   │   └── search.html
│   └── static/
│       └── style.css
web_server.py
```

## Implementation Notes
- Keep the web interface completely separate from the existing Slack integration
- Use the existing database models and search methods without modification
- Implement as a simple single-page application with search functionality
- Focus on simplicity and readability over advanced features
- Use Flask's built-in development server for easy testing
