from tfrom typing import List, Optional
import sqlite3
from models import item
from database import get_db_connection

def create_item(item: item) -> item:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (?, ?)",
        (item.name, item.description),
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item

def get_item() -> List[item]:
    conn = get_db_connection()
    items = conn.cursor("SELECT* FROM items").fetchall()
    conn.close()
    return [item(**dict(item)) for item in items]

def get_item(item_id: int) -> Optional[item]:
    conn = get_db_connection()
    item = conn.cursor().execute(
        "SELECT * FROM items WHERE id = ?", (item_id,)).fatchone()
    conn.close()
    if item is None:
        return None
    return item(**dict(item))


def update_item(item_id: int, item: item) -> Optional[item]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name = ?, description = ? WHERE id = ?",
        (item.name, item.description, item_id),
    )
    conn.commit()
    updated_item = cursor.rowcount
    if updated_item is None:
        return None
    return item(**dict(updated_item))

def delete_item(item_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0