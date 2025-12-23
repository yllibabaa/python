"""SQLite database helpers.

The original project used SQLite with a small connection helper and a startup
initializer that creates tables.

This project keeps that approach but adds:
- Separate `ratings` table (so averages are computed, not stored)
- SQLite foreign keys enabled
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "videogames.db")).resolve()


def get_db_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row access by name and FK support."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_database() -> None:
    """Create database tables if they don't exist."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS studios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            studio_id INTEGER NOT NULL,
            release_year INTEGER,
            platforms TEXT,          -- comma-separated
            genres TEXT,             -- comma-separated
            cover_url TEXT,
            UNIQUE(title, studio_id),
            FOREIGN KEY(studio_id) REFERENCES studios(id) ON DELETE CASCADE
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            score INTEGER NOT NULL CHECK(score >= 1 AND score <= 10),
            username TEXT,
            comment TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(game_id) REFERENCES games(id) ON DELETE CASCADE
        );
        """
    )

    conn.commit()
    conn.close()
