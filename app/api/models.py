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

    class Config:
        from_attributes = True

class ProductUpdate_sc(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    main_photo: Optional[str] = None
    additional_photos: Optional[List[str]] = None

    class Config:
        from_attributes = True

class Category_sc(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

class CartItem_sc(BaseModel):
    id: Optional[int] = None
    product_id: int
    quantity: int
    product: Optional[Product_sc] = None

    class Config:
        from_attributes = True

class Cart_sc(BaseModel):
    id: Optional[int] = None
    session_id: str
    created_at: str
    items: List[CartItem_sc] = []

    class Config:
        from_attributes = True