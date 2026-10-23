# main.py

from fastapi import FastAPI
from typing import Annotated
from fastapi import Path, Query


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str):
    return {"user_id": user_id, "item_id": item_id}

fake_items_db = [
    {"name": "Laptop"},
    {"name": "Mouse"},
    {"name": "Keyboard"},
    {"name": "Monitor"},
    {"name": "Headphones"},
    {"name": "Phone"}
]

@app.get("/items/")
async def read_items(
    skip: int = 0,
    limit: int = 10
):
    return fake_items_db[skip:skip + limit]

@app.get("/search/")
async def search_items(q: str | None = None):
    if q:
        return {"query": q}
    return {"message": "No query provided"}




@app.get("/products/{product_id}")
async def get_product(
    product_id: Annotated[int, Path(gt=0)],
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):                return {"product_id": product_id, "q": q, "limit": limit}





