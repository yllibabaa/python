from fastapi import FastAPI, HTTPException, Depends
from typing import List
from crudc import create_item, get_item, get_items, update_item, delete_item
from modelsc import item
from securityc import get_api_key
from databasec import init_db

app = FastAPI()
init_db()

@app.post("/items/", response_model=item)
def create_new_item(item_data: item, api_key: str = Depends(get_api_key)):
    return create_item(item_data)
