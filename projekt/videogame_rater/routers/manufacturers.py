"""Manufacturers API router (CRUD). 

Public:
- GET /manufacturers

Admin (API key required):
- POST /manufacturers
- PUT /manufacturers/{id}
- DELETE /manufacturers/{id}
"""

from __future__ import annotations

import sqlite3
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from auth.security import get_api_key
from database import get_db_connection
from models.manufacturer import Manufacturer, ManufacturerCreate

router = APIRouter()


@router.get("/", response_model=List[Manufacturer])
def list_manufacturers() -> List[Manufacturer]:
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name FROM manufacturers ORDER BY name").fetchall()
    conn.close()
    return [Manufacturer(id=r["id"], name=r["name"]) for r in rows]


@router.post("/", response_model=Manufacturer)
def create_manufacturer(payload: ManufacturerCreate, _: str = Depends(get_api_key)) -> Manufacturer:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO manufacturers (name) VALUES (?)", (payload.name.strip(),))
        conn.commit()
        manufacturer_id = cur.lastrowid
        return Manufacturer(id=manufacturer_id, name=payload.name.strip())
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Manufacturer '{payload.name}' already exists.",
        )
    finally:
        conn.close()


@router.put("/{manufacturer_id}", response_model=Manufacturer)
def update_manufacturer(manufacturer_id: int, payload: ManufacturerCreate, _: str = Depends(get_api_key)) -> Manufacturer:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE manufacturers SET name = ? WHERE id = ?", (payload.name.strip(), manufacturer_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        conn.commit()
        return Manufacturer(id=manufacturer_id, name=payload.name.strip())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Manufacturer name already exists")
    finally:
        conn.close()


@router.delete("/{manufacturer_id}", response_model=dict)
def delete_manufacturer(manufacturer_id: int, _: str = Depends(get_api_key)) -> dict:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM manufacturers WHERE id = ?", (manufacturer_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    conn.commit()
    conn.close()
    return {"detail": "Manufacturer deleted"}
