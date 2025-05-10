from pydantic import BaseModel
from typing import Optional, List

class Product_sc(BaseModel):
    id: Optional[int] = None
    category_id: int
    title: str
    description: str
    price: float
    main_photo: Optional[str] = None
    additional_photos: Optional[List[str]] = None

class ProductUpdate_sc(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    main_photo: Optional[str] = None
    additional_photos: Optional[List[str]] = None

class Category_sc(BaseModel):
    id: Optional[int] = None
    name: str