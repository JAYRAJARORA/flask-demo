# to run this file 
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel
from typing import List

app = FastAPI()

# MongoDB client setup for all operations, automatically handles primary selection
client = MongoClient(
    "mongodb://localhost:27018,localhost:27019,localhost:27020",
    replicaSet='rs0',
    readPreference='secondaryPreferred'  # Fallback to primary if no secondaries are available
)

db = client.testdb  # Use the same db client for reads and writes

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float


def item_to_model(item):
    return ItemResponse(
        id=str(item["_id"]),
        name=item["name"],
        description=item.get("description"),
        price=item["price"]
    )



@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    result = db.items.insert_one(item.dict())
    item_id = result.inserted_id
    new_item = db.items.find_one({"_id": item_id})
    if new_item:
        return item_to_model(new_item)
    raise HTTPException(status_code=404, detail="Item not found after insertion")

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: str):
    try:
        _id = ObjectId(item_id)  # Convert string to ObjectId
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid item ID format: {str(e)}")

    item = db.items.find_one({"_id": _id})
    print("Read from:", client.address, "Read Pref:", db.read_preference)

    if item:
        return item_to_model(item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items", response_model=List[ItemResponse])
async def read_items():
    items = list(db.items.find())
    return [item_to_model(item) for item in items]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
