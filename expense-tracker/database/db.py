import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DATABASE_PATH = Path(__file__).parent.parent / "spendly.db"


def get_db():
    """Return a SQLite connection with row_factory and foreign_keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        return  # Already seeded

    # Insert demo user with hashed password
    password_hash = generate_password_hash("demo123")
    cursor.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    """, ("Demo User", "demo@spendly.com", password_hash))

    # Insert 8 sample expenses covering all categories
    expenses = [
        (1, 50.00, "Food", "2026-04-01", "Groceries at supermarket"),
        (1, 25.00, "Transport", "2026-04-02", "Uber ride to work"),
        (1, 120.00, "Bills", "2026-04-05", "Electric bill"),
        (1, 45.00, "Health", "2026-04-08", "Pharmacy prescription"),
        (1, 35.00, "Entertainment", "2026-04-10", "Movie tickets"),
        (1, 89.99, "Shopping", "2026-04-12", "New shirt and jeans"),
        (1, 15.00, "Other", "2026-04-15", "Coffee shop"),
        (1, 60.00, "Food", "2026-04-18", "Dinner with friends"),
    ]

    cursor.executemany("""
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, expenses)

    conn.commit()
    conn.close()
