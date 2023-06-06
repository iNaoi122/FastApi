import datetime
from enum import Enum
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="FastApi")

list_users = [
    {"id": 1, "role": 'admin', "name": "Bob"},
    {"id": 2, "role": "trader", "name": 'Sam'},
    {"id": 3, "role": "investor", "name": "John"},
    {"id":4, 'role':"investor", "name":"Homer"},
]

list_traders = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 2, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    create_at: datetime.datetime
    type_degree: str


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
async def root(user_id: int):
    return [user for user in list_users if user.get("id") == user_id]


@app.get("/trades")
async def get_trades(limit: int = 1, offset: int = 0):
    return list_traders[offset:][:limit]


@app.post("/users/{users_id}")
async def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, list_users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
async def add_traders(trades: List[Trade]):
    list_traders.extend(trades)
    return {"status": 200, "data": list_traders}

