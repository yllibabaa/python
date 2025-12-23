"""Airplanes API router.

Public:
- GET /airplanes
- GET /airplanes/{airplane_id}
- GET /airplanes/leaderboard/top

Admin (API key required):
- POST /airplanes
- PUT /airplanes/{airplane_id}
- DELETE /airplanes/{airplane_id}

Averages are computed from the `ratings` table.
"""

from __future__ import annotations

import sqlite3
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.security import get_api_key
from database import get_db_connection
from models.airplane import Airplane, AirplaneCreate

router = APIRouter()


def _row_to_airplane(row) -> Airplane:
    return Airplane(
        id=row["id"],
        model=row["model"],
        manufacturer_id=row["manufacturer_id"],
        manufacture_year=row["manufacture_year"],
        capacity=row["capacity"],
        types=[t for t in (row["types"] or "").split(",") if t],
        image_url=row["image_url"],
        average_score=float(row["average_score"] or 0.0),
        ratings_count=int(row["ratings_count"] or 0),
    )


@router.get("/", response_model=List[Airplane])
def list_airplanes(
    q: Optional[str] = Query(default=None, description="Search in airplane models"),
    manufacturer_id: Optional[int] = Query(default=None, ge=1),
    min_year: Optional[int] = Query(default=None, ge=1903, le=2100),
    max_year: Optional[int] = Query(default=None, ge=1903, le=2100),
) -> List[Airplane]:
    """List airplanes with computed averages."""
    conn = get_db_connection()

    where: list[str] = []
    params: list = []

    if q:
        where.append("a.model LIKE ?")
        params.append(f"%{q}%")
    if manufacturer_id:
        where.append("a.manufacturer_id = ?")
        params.append(manufacturer_id)
    if min_year is not None:
        where.append("a.manufacture_year >= ?")
        params.append(min_year)
    if max_year is not None:
        where.append("a.manufacture_year <= ?")
        params.append(max_year)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    rows = conn.execute(
        f"""
        SELECT
            a.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM airplanes a
        LEFT JOIN ratings r ON r.airplane_id = a.id
        {where_sql}
        GROUP BY a.id
        ORDER BY COALESCE(average_score, 0) DESC, ratings_count DESC, a.model ASC
        """,
        params,
    ).fetchall()

    conn.close()
    return [_row_to_airplane(r) for r in rows]


@router.get("/{airplane_id}", response_model=Airplane)
def get_airplane(airplane_id: int) -> Airplane:
    """Get a single airplane (with computed average)."""
    conn = get_db_connection()
    row = conn.execute(
        """
        SELECT
            a.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM airplanes a
        LEFT JOIN ratings r ON r.airplane_id = a.id
        WHERE a.id = ?
        GROUP BY a.id
        """,
        (airplane_id,),
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Airplane not found")

    return _row_to_airplane(row)


@router.get("/leaderboard/top", response_model=List[Airplane])
def leaderboard_top(
    limit: int = Query(default=10, ge=1, le=100),
    min_votes: int = Query(default=3, ge=0, le=10000),
) -> List[Airplane]:
    """Top airplanes by average score, with a minimum number of ratings."""
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT
            a.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM airplanes a
        JOIN ratings r ON r.airplane_id = a.id
        GROUP BY a.id
        HAVING COUNT(r.id) >= ?
        ORDER BY average_score DESC, ratings_count DESC, a.model ASC
        LIMIT ?
        """,
        (min_votes, limit),
    ).fetchall()
    conn.close()
    return [_row_to_airplane(r) for r in rows]


@router.post("/", response_model=Airplane, status_code=status.HTTP_201_CREATED)
def create_airplane(payload: AirplaneCreate, _: str = Depends(get_api_key)) -> Airplane:
    """Create an airplane (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        types = ",".join([t.strip() for t in payload.types if t.strip()])
        cur.execute(
            """
            INSERT INTO airplanes (model, manufacturer_id, manufacture_year, capacity, types, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload.model.strip(),
                payload.manufacturer_id,
                payload.manufacture_year,
                payload.capacity,
                types,
                str(payload.image_url) if payload.image_url else None,
            ),
        )
        conn.commit()
        airplane_id = cur.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Airplane already exists for this manufacturer.")
    finally:
        conn.close()

    return get_airplane(airplane_id)


@router.put("/{airplane_id}", response_model=Airplane)
def update_airplane(airplane_id: int, payload: AirplaneCreate, _: str = Depends(get_api_key)) -> Airplane:
    """Update an airplane (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    types = ",".join([t.strip() for t in payload.types if t.strip()])
    try:
        cur.execute(
            """
            UPDATE airplanes
            SET model = ?, manufacturer_id = ?, manufacture_year = ?, capacity = ?, types = ?, image_url = ?
            WHERE id = ?
            """,
            (
                payload.model.strip(),
                payload.manufacturer_id,
                payload.manufacture_year,
                payload.capacity,
                types,
                str(payload.image_url) if payload.image_url else None,
                airplane_id,
            ),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Airplane not found")
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An airplane with this model already exists for that manufacturer.",
        )
    finally:
        conn.close()

    return get_airplane(airplane_id)


@router.delete("/{airplane_id}", response_model=dict)
def delete_airplane(airplane_id: int, _: str = Depends(get_api_key)) -> dict:
    """Delete an airplane (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM airplanes WHERE id = ?", (airplane_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Airplane not found")
    conn.commit()
    conn.close()
    return {"detail": "Airplane deleted"}
