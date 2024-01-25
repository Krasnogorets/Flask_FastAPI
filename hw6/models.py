import datetime

from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    name: str = Field(max_length=32, min_length=3)
    secondname: str = Field(max_length=32, min_length=5)
    email: EmailStr = Field(max_length=60)


class User(BaseModel):
    id: int
    name: str = Field(..., max_length=32, min_length=2)
    secondname: str = Field(..., max_length=32, min_length=2)
    email: EmailStr = Field(..., max_length=60)
    password: str = Field(..., max_length=64)


class Orders(BaseModel):
    id: int
    user_id: int
    goods_id: int
    date: datetime
    status: str = Field(..., max_length=32)


class Goods(BaseModel):
    id: int
    title: str = Field(..., max_length=32, min_length=2)
    description: str = Field(default=None, max_length=500)
    price: float = Field(..., gt=0, le=100_000)


class GoodsIn(BaseModel):
    title: str = Field(..., max_length=32, min_length=2)
    description: str = Field(default=None, max_length=500)
    price: float = Field(..., gt=0, le=100_000)

