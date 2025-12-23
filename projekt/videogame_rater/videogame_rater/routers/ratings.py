"""Ratings (reviews) API router.

Public:
- POST /ratings           create a rating for a game
- GET  /ratings           list ratings (filter by game_id)
- GET  /ratings/recent    recent ratings

Admin:
- DELETE /ratings/{id}    remove abusive ratings (API key)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.security import get_api_key
from database import get_db_connection
from models.rating import Rating, RatingCreate

router = APIRouter()


def _row_to_rating(row) -> Rating:
    return Rating(
        id=row["id"],
        game_id=row["game_id"],
        score=row["score"],
        username=row["username"],
        comment=row["comment"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


@router.post("/", response_model=Rating, status_code=status.HTTP_201_CREATED)
def create_rating(payload: RatingCreate) -> Rating:
    """Create a rating (public endpoint)."""
    conn = get_db_connection()
    # Ensure game exists
    game = conn.execute("SELECT id FROM games WHERE id = ?", (payload.game_id,)).fetchone()
    if not game:
        conn.close()
        raise HTTPException(status_code=404, detail="Game not found")

    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO ratings (game_id, score, username, comment, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (payload.game_id, payload.score, payload.username, payload.comment, created),
    )
    conn.commit()
    rating_id = cur.lastrowid

    row = conn.execute(
        "SELECT id, game_id, score, username, comment, created_at FROM ratings WHERE id = ?",
        (rating_id,),
    ).fetchone()
    conn.close()
    return _row_to_rating(row)


@router.get("/", response_model=List[Rating])
def list_ratings(
    game_id: Optional[int] = Query(default=None, ge=1),
    limit: int = Query(default=50, ge=1, le=500),
) -> List[Rating]:
    """List ratings, optionally filtered by game."""
    conn = get_db_connection()

    if game_id:
        rows = conn.execute(
            """
            SELECT id, game_id, score, username, comment, created_at
            FROM ratings
            WHERE game_id = ?
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (game_id, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT id, game_id, score, username, comment, created_at
            FROM ratings
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    conn.close()
    return [_row_to_rating(r) for r in rows]


@router.get("/recent", response_model=List[Rating])
def recent_ratings(limit: int = Query(default=20, ge=1, le=200)) -> List[Rating]:
    """Convenience endpoint for homepage widgets."""
    return list_ratings(game_id=None, limit=limit)


@router.delete("/{rating_id}", response_model=dict)
def delete_rating(rating_id: int, _: str = Depends(get_api_key)) -> dict:
    """Delete a rating (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ratings WHERE id = ?", (rating_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Rating not found")
    conn.commit()
    conn.close()
    return {"detail": "Rating deleted"}
