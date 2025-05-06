from pydantic import BaseModel
from typing import Optional, List

class Product_sc(BaseModel):
    id: Optional[int] = None
    category_id: int
    title: str
    description: str
    price: float
    photos: Optional[List[str]] = None  # список путей к фото

class ProductUpdate_sc(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    photos: Optional[List[str]] = None

class Category_sc(BaseModel):
    id: Optional[int] = None
    name: str