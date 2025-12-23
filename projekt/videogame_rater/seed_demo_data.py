"""Seed the database with a small set of demo manufacturers and airplanes.

This is intentionally offline (no scraping / no external APIs).

Usage:
    python seed_demo_data.py

It will only insert items that don't already exist.
"""

from __future__ import annotations

from database import create_database, get_db_connection

DEMO = {
    "Boeing": [
        {
            "model": "747-8",
            "manufacture_year": 2011,
            "capacity": 467,
            "types": ["Passenger"],
            "image_url": None,
        },
        {
            "model": "737 MAX",
            "manufacture_year": 2017,
            "capacity": 210,
            "types": ["Passenger"],
            "image_url": None,
        },
    ],
    "Airbus": [
        {
            "model": "A380",
            "manufacture_year": 2007,
            "capacity": 555,
            "types": ["Passenger"],
            "image_url": None,
        },
        {
            "model": "A320",
            "manufacture_year": 1987,
            "capacity": 180,
            "types": ["Passenger"],
            "image_url": None,
        },
    ],
    "Cessna": [
        {
            "model": "172 Skyhawk",
            "manufacture_year": 1956,
            "capacity": 4,
            "types": ["Private"],
            "image_url": None,
        },
    ],
}


def main() -> None:
    create_database()
    conn = get_db_connection()
    cur = conn.cursor()

    for manufacturer_name, airplanes in DEMO.items():
        cur.execute("INSERT OR IGNORE INTO manufacturers (name) VALUES (?)", (manufacturer_name,))
        manufacturer_id = conn.execute("SELECT id FROM manufacturers WHERE name = ?", (manufacturer_name,)).fetchone()["id"]

        for a in airplanes:
            cur.execute(
                """
                INSERT OR IGNORE INTO airplanes (model, manufacturer_id, manufacture_year, capacity, types, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    a["model"],
                    manufacturer_id,
                    a.get("manufacture_year"),
                    a.get("capacity"),
                    ",".join(a.get("types", [])),
                    a.get("image_url"),
                ),
            )

    conn.commit()
    conn.close()
    print("Seeded demo data (if missing).")


if __name__ == "__main__":
    main()
