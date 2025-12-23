"""Seed the database with a small set of demo studios and games.

This is intentionally offline (no scraping / no external APIs).

Usage:
    python seed_demo_data.py

It will only insert items that don't already exist.
"""

from __future__ import annotations

from database import create_database, get_db_connection

DEMO = {
    "Nintendo": [
        {
            "title": "The Legend of Zelda: Breath of the Wild",
            "release_year": 2017,
            "platforms": ["Switch"],
            "genres": ["Action", "Adventure"],
            "cover_url": None,
        },
        {
            "title": "Super Mario Odyssey",
            "release_year": 2017,
            "platforms": ["Switch"],
            "genres": ["Platformer"],
            "cover_url": None,
        },
    ],
    "FromSoftware": [
        {
            "title": "Elden Ring",
            "release_year": 2022,
            "platforms": ["PC", "PS5", "Xbox"],
            "genres": ["RPG", "Action"],
            "cover_url": None,
        },
    ],
    "CD Projekt Red": [
        {
            "title": "The Witcher 3: Wild Hunt",
            "release_year": 2015,
            "platforms": ["PC", "PS5", "Xbox", "Switch"],
            "genres": ["RPG"],
            "cover_url": None,
        },
    ],
}


def main() -> None:
    create_database()
    conn = get_db_connection()
    cur = conn.cursor()

    for studio_name, games in DEMO.items():
        cur.execute("INSERT OR IGNORE INTO studios (name) VALUES (?)", (studio_name,))
        studio_id = conn.execute("SELECT id FROM studios WHERE name = ?", (studio_name,)).fetchone()["id"]

        for g in games:
            cur.execute(
                """
                INSERT OR IGNORE INTO games (title, studio_id, release_year, platforms, genres, cover_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    g["title"],
                    studio_id,
                    g.get("release_year"),
                    ",".join(g.get("platforms", [])),
                    ",".join(g.get("genres", [])),
                    g.get("cover_url"),
                ),
            )

    conn.commit()
    conn.close()
    print("Seeded demo data (if missing).")


if __name__ == "__main__":
    main()
