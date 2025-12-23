"""Studios API router (CRUD).

Public:
- GET /studios

Admin (API key required):
- POST /studios
- PUT /studios/{id}
- DELETE /studios/{id}
"""

from __future__ import annotations

import sqlite3
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from auth.security import get_api_key
from database import get_db_connection
from models.studio import Studio, StudioCreate

router = APIRouter()


@router.get("/", response_model=List[Studio])
def list_studios() -> List[Studio]:
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name FROM studios ORDER BY name").fetchall()
    conn.close()
    return [Studio(id=r["id"], name=r["name"]) for r in rows]


@router.post("/", response_model=Studio)
def create_studio(payload: StudioCreate, _: str = Depends(get_api_key)) -> Studio:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO studios (name) VALUES (?)", (payload.name.strip(),))
        conn.commit()
        studio_id = cur.lastrowid
        return Studio(id=studio_id, name=payload.name.strip())
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Studio '{payload.name}' already exists.",
        )
    finally:
        conn.close()


@router.put("/{studio_id}", response_model=Studio)
def update_studio(studio_id: int, payload: StudioCreate, _: str = Depends(get_api_key)) -> Studio:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE studios SET name = ? WHERE id = ?", (payload.name.strip(), studio_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Studio not found")
        conn.commit()
        return Studio(id=studio_id, name=payload.name.strip())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Studio name already exists")
    finally:
        conn.close()


@router.delete("/{studio_id}", response_model=dict)
def delete_studio(studio_id: int, _: str = Depends(get_api_key)) -> dict:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM studios WHERE id = ?", (studio_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Studio not found")
    conn.commit()
    conn.close()
    return {"detail": "Studio deleted"}
