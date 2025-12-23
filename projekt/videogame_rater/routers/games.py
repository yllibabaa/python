"""Games API router.

Public:
- GET /games
- GET /games/{game_id}
- GET /games/leaderboard/top

Admin (API key required):
- POST /games
- PUT /games/{game_id}
- DELETE /games/{game_id}

Averages are computed from the `ratings` table.
"""

from __future__ import annotations

import sqlite3
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.security import get_api_key
from database import get_db_connection
from models.game import Game, GameCreate

router = APIRouter()


def _row_to_game(row) -> Game:
    return Game(
        id=row["id"],
        title=row["title"],
        studio_id=row["studio_id"],
        release_year=row["release_year"],
        platforms=[p for p in (row["platforms"] or "").split(",") if p],
        genres=[g for g in (row["genres"] or "").split(",") if g],
        cover_url=row["cover_url"],
        average_score=float(row["average_score"] or 0.0),
        ratings_count=int(row["ratings_count"] or 0),
    )

from auth.security import get_api_key
from database import get_db_connection
from models.game import Game, GameCreate

router = APIRouter()


def _row_to_game(row) -> Game:
    """Convert a sqlite row to the public Game model."""
    return Game(
        id=row["id"],
        title=row["title"],
        studio_id=row["studio_id"],
        release_year=row["release_year"],
        platforms=[p for p in (row["platforms"] or "").split(",") if p],
        genres=[g for g in (row["genres"] or "").split(",") if g],
        cover_url=row["cover_url"],
        average_score=float(row["average_score"] or 0.0),
        ratings_count=int(row["ratings_count"] or 0),
    )

from auth.security import get_api_key
from database import get_db_connection
from models.game import Game, GameCreate

router = APIRouter()


def _row_to_game(row) -> Game:
    """Convert a sqlite row to the public Game model."""
    return Game(
        id=row["id"],
        title=row["title"],
        studio_id=row["studio_id"],
        release_year=row["release_year"],
        platforms=[p for p in (row["platforms"] or "").split(",") if p],
        genres=[g for g in (row["genres"] or "").split(",") if g],
        cover_url=row["cover_url"],
        average_score=float(row["average_score"] or 0.0),
        ratings_count=int(row["ratings_count"] or 0),
    )


@router.get("/", response_model=List[Game])
def list_games(
    q: Optional[str] = Query(default=None, description="Search in game titles"),
    studio_id: Optional[int] = Query(default=None, ge=1),
    min_year: Optional[int] = Query(default=None, ge=1970, le=2100),
    max_year: Optional[int] = Query(default=None, ge=1970, le=2100),
) -> List[Game]:
    """List games with computed averages."""
    conn = get_db_connection()

    where: list[str] = []
    params: list = []

    if q:
        where.append("g.title LIKE ?")
        params.append(f"%{q}%")
    if studio_id:
        where.append("g.studio_id = ?")
        params.append(studio_id)
    if min_year is not None:
        where.append("g.release_year >= ?")
        params.append(min_year)
    if max_year is not None:
        where.append("g.release_year <= ?")
        params.append(max_year)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    rows = conn.execute(
        f"""
        SELECT
            g.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM games g
        LEFT JOIN ratings r ON r.game_id = g.id
        {where_sql}
        GROUP BY g.id
        ORDER BY COALESCE(average_score, 0) DESC, ratings_count DESC, g.title ASC
        """,
        params,
    ).fetchall()

    conn.close()
    return [_row_to_game(r) for r in rows]


@router.get("/", response_model=List[Game])
def list_games(
    q: Optional[str] = Query(default=None, description="Search in game titles"),
    studio_id: Optional[int] = Query(default=None, ge=1),
    min_year: Optional[int] = Query(default=None, ge=1970, le=2100),
    max_year: Optional[int] = Query(default=None, ge=1970, le=2100),
) -> List[Game]:
    """List games with computed averages."""
    conn = get_db_connection()


@router.get("/", response_model=List[Game])
def list_games(
    q: Optional[str] = Query(default=None, description="Search in game titles"),
    studio_id: Optional[int] = Query(default=None, ge=1),
    min_year: Optional[int] = Query(default=None, ge=1970, le=2100),
    max_year: Optional[int] = Query(default=None, ge=1970, le=2100),
) -> List[Game]:
    """List games with computed averages."""
    conn = get_db_connection()

    where = []
    params: list = []

    if q:
        where.append("g.title LIKE ?")
        params.append(f"%{q}%")
    if studio_id:
        where.append("g.studio_id = ?")
        params.append(studio_id)
    if min_year is not None:
        where.append("g.release_year >= ?")
        params.append(min_year)
    if max_year is not None:
        where.append("g.release_year <= ?")
        params.append(max_year)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    rows = conn.execute(
        f"""
        SELECT
            g.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM games g
        LEFT JOIN ratings r ON r.game_id = g.id
        {where_sql}
        GROUP BY g.id
        ORDER BY COALESCE(average_score, 0) DESC, ratings_count DESC, g.title ASC
        """,
        params,
    ).fetchall()

    conn.close()
    return [_row_to_game(r) for r in rows]


@router.get("/{game_id}", response_model=Game)
def get_game(game_id: int) -> Game:
    """Get a single game (with computed average)."""
    conn = get_db_connection()
    row = conn.execute(
        """
        SELECT
            g.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM games g
        LEFT JOIN ratings r ON r.game_id = g.id
        WHERE g.id = ?
        GROUP BY g.id
        """,
        (game_id,),
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Game not found")

    return _row_to_game(row)


@router.get("/leaderboard/top", response_model=List[Game])
def leaderboard_top(
    limit: int = Query(default=10, ge=1, le=100),
    min_votes: int = Query(default=3, ge=0, le=10000),
) -> List[Game]:
    """Top games by average score, with a minimum number of ratings."""
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT
            g.*,
            AVG(r.score) AS average_score,
            COUNT(r.id) AS ratings_count
        FROM games g
        JOIN ratings r ON r.game_id = g.id
        GROUP BY g.id
        HAVING COUNT(r.id) >= ?
        ORDER BY average_score DESC, ratings_count DESC, g.title ASC
        LIMIT ?
        """,
        (min_votes, limit),
    ).fetchall()
    conn.close()
    return [_row_to_game(r) for r in rows]


@router.post("/", response_model=Game, status_code=status.HTTP_201_CREATED)
def create_game(payload: GameCreate, _: str = Depends(get_api_key)) -> Game:
    """Create a game (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        platforms = ",".join([p.strip() for p in payload.platforms if p.strip()])
        genres = ",".join([g.strip() for g in payload.genres if g.strip()])
        cur.execute(
            """
            INSERT INTO games (title, studio_id, release_year, platforms, genres, cover_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload.title.strip(),
                payload.studio_id,
                payload.release_year,
                platforms,
                genres,
                str(payload.cover_url) if payload.cover_url else None,
            ),
        )
        conn.commit()
        game_id = cur.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game already exists for this studio.")
    finally:
        conn.close()

    return get_game(game_id)


@router.put("/{game_id}", response_model=Game)
def update_game(game_id: int, payload: GameCreate, _: str = Depends(get_api_key)) -> Game:
    """Update a game (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    platforms = ",".join([p.strip() for p in payload.platforms if p.strip()])
    genres = ",".join([g.strip() for g in payload.genres if g.strip()])
    try:
        cur.execute(
            """
            UPDATE games
            SET title = ?, studio_id = ?, release_year = ?, platforms = ?, genres = ?, cover_url = ?
            WHERE id = ?
            """,
            (
                payload.title.strip(),
                payload.studio_id,
                payload.release_year,
                platforms,
                genres,
                str(payload.cover_url) if payload.cover_url else None,
                game_id,
            ),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Game not found")
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A game with this title already exists for that studio.",
        )
    finally:
        conn.close()

    return get_game(game_id)


@router.delete("/{game_id}", response_model=dict)
def delete_game(game_id: int, _: str = Depends(get_api_key)) -> dict:
    """Delete a game (admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE id = ?", (game_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Game not found")
    conn.commit()
    conn.close()
    return {"detail": "Game deleted"}
