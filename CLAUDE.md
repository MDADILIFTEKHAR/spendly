# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly - A Flask-based expense tracking web application. Currently a student project with scaffolding in place for core features.

## Commands

```bash
# Run the application
python expense-tracker/app.py

# Install dependencies
pip install -r expense-tracker/requirements.txt

# Run tests (pytest configured with flask plugin)
pytest
```

## Architecture

- **Flask app** (`expense-tracker/app.py`) - Main application with routes for landing, auth (login/register/logout), and expense CRUD placeholders
- **Database** (`expense-tracker/database/db.py`) - SQLite with `get_db()`, `init_db()`, `seed_db()` functions (to be implemented)
- **Templates** - Jinja2 HTML templates extending `base.html` with a consistent navbar/footer layout
- **Static assets** - CSS variables-based styling in `static/css/style.css`, JavaScript in `static/js/main.js`
- **Database file** - `expense_tracker.db` (gitignored)

## Key Patterns

- Routes render templates or return placeholder strings for features not yet implemented
- Base template provides navbar (with conditional auth links) and footer
- SQLite connections should have `row_factory` and `foreign_keys` enabled
