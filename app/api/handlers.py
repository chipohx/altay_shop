from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.api.models import Product_sc, ProductUpdate_sc, Category_sc
from app.api.actions.products import (
    _create_new_product,
    _create_new_category,
    _delete_category,
    _delete_product,
    _get_product_by_id,
    _get_all_products,
    _get_search_products,
    _update_product
)

product_router = APIRouter(prefix="/api/v1", tags=["products"])

# Product endpoints
@product_router.post("/products", response_model=Product_sc)
async def create_product(
    product_data: Product_sc,
    db: AsyncSession = Depends(get_db)
):
    return await _create_new_product(product_data, db)

@product_router.get("/products/{product_id}", response_model=Product_sc)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await _get_product_by_id(product_id, db)

@product_router.get("/products", response_model=List[Product_sc])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    return await _get_all_products(db)

@product_router.get("/products/search", response_model=List[Product_sc])
async def search_products(
    q: str | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await _get_search_products(db, search_term=q)

@product_router.patch("/products/{product_id}", response_model=Product_sc)
async def update_product(
    product_id: int,
    update_data: ProductUpdate_sc = Body(...),
    db: AsyncSession = Depends(get_db)
):
    return await _update_product(product_id, db, update_data)

@product_router.delete("/products/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    await _delete_product(product_id, db)
    return {}

# Category endpoints
@product_router.post("/categories", response_model=Category_sc)
async def create_category(
    category_data: Category_sc,
    db: AsyncSession = Depends(get_db)
):
    return await _create_new_category(category_data, db)

@product_router.get("/categories", response_model=List[Category_sc])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    from app.db.models import Categories
    result = await db.execute(select(Categories))
    categories = result.scalars().all()
    return [Category_sc(id=cat.id, name=cat.name) for cat in categories]

@product_router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    await _delete_category(category_id, db)
    return {}