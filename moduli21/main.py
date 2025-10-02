from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/items/")
def read_root():
    return {"items": ["item1", "item2", "item3"]}
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{user_id}")
def read_users(user_id: int):
    return {"users": user_id, "name": "John Doe"}

@app.post("/items")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str = None, price: float = None):
    return {"item_id": item_id, "name": name, "price": price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
