from fastapi import APIRouter, Depends, Body, Query, HTTPException, Form, UploadFile, File, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os

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
from app.db.models import Categories

# Шаблоны для всех роутеров
templates = Jinja2Templates(directory="app/templates")

# API роутер для публичного API
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

# Роутер для фронтенд-маршрутов
frontend_router = APIRouter(tags=["frontend"])

@frontend_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@frontend_router.get("/product/{product_id}")
async def product_detail(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        product = await _get_product_by_id(product_id, db)
        return templates.TemplateResponse("product_detail.html", {
            "request": request, 
            "product_id": product_id,
            "product": product
        })
    except:
        # В случае ошибки просто передаем product_id
        return templates.TemplateResponse("product_detail.html", {"request": request, "product_id": product_id})

@frontend_router.get("/categories")
async def categories(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})

# Административный роутер
admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("")
async def admin_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    products = await _get_all_products(db)
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "products": products})

@admin_router.get("/products")
async def admin_products(request: Request, db: AsyncSession = Depends(get_db)):
    products = await _get_all_products(db)
    return templates.TemplateResponse("admin/products.html", {"request": request, "products": products})

@admin_router.get("/products/new")
async def admin_new_product_form(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Categories))
    categories = result.scalars().all()
    
    return templates.TemplateResponse("admin/product_form.html", {
        "request": request, 
        "categories": categories,
        "product": None
    })

@admin_router.post("/products/new")
async def admin_create_product(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    main_photo: UploadFile = File(None),
    additional_photos: List[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    main_photo_path = None
    additional_photo_paths = []
    
    # Обработка главного фото
    if main_photo and main_photo.filename:
        file_path = f"app/static/uploads/{main_photo.filename}"
        with open(file_path, "wb") as f:
            f.write(await main_photo.read())
        main_photo_path = f"/static/uploads/{main_photo.filename}"
    
    # Обработка дополнительных фото
    if additional_photos:
        for photo in additional_photos:
            if photo.filename:
                file_path = f"app/static/uploads/{photo.filename}"
                with open(file_path, "wb") as f:
                    f.write(await photo.read())
                additional_photo_paths.append(f"/static/uploads/{photo.filename}")
    
    product_data = Product_sc(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        main_photo=main_photo_path,
        additional_photos=additional_photo_paths if additional_photo_paths else None
    )
    
    await _create_new_product(product_data, db)
    return RedirectResponse(url="/admin/products", status_code=303)

@admin_router.get("/products/{product_id}/edit")
async def admin_edit_product_form(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    product = await _get_product_by_id(product_id, db)
    
    result = await db.execute(select(Categories))
    categories = result.scalars().all()
    
    return templates.TemplateResponse("admin/product_form.html", {
        "request": request, 
        "product": product,
        "categories": categories
    })

@admin_router.post("/products/{product_id}/edit")
async def admin_update_product(
    request: Request,
    product_id: int,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    main_photo: UploadFile = File(None),
    additional_photos: List[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    # Получаем текущий продукт
    current_product = await _get_product_by_id(product_id, db)
    
    # Получаем текущий главный путь к фото или None
    main_photo_path = current_product.main_photo
    
    # Обрабатываем новое главное фото, если оно есть
    if main_photo and main_photo.filename:
        file_path = f"app/static/uploads/{main_photo.filename}"
        with open(file_path, "wb") as f:
            f.write(await main_photo.read())
        main_photo_path = f"/static/uploads/{main_photo.filename}"
    
    # Получаем текущие дополнительные фото или пустой список
    current_additional_photos = current_product.additional_photos or []
    
    # Обрабатываем новые дополнительные фото, если они есть
    new_photo_paths = []
    if additional_photos:
        for photo in additional_photos:
            if photo.filename:
                file_path = f"app/static/uploads/{photo.filename}"
                with open(file_path, "wb") as f:
                    f.write(await photo.read())
                new_photo_paths.append(f"/static/uploads/{photo.filename}")
    
    # Объединяем существующие и новые дополнительные фото
    all_additional_photos = current_additional_photos + new_photo_paths if new_photo_paths else current_additional_photos
    
    update_data = ProductUpdate_sc(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        main_photo=main_photo_path,
        additional_photos=all_additional_photos if all_additional_photos else None
    )
    
    await _update_product(product_id, db, update_data)
    return RedirectResponse(url="/admin/products", status_code=303)

@admin_router.get("/products/{product_id}/delete")
async def admin_delete_product(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    await _delete_product(product_id, db)
    return RedirectResponse(url="/admin/products", status_code=303)

@admin_router.get("/categories")
async def admin_categories(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Categories))
    categories = result.scalars().all()
    
    return templates.TemplateResponse("admin/categories.html", {"request": request, "categories": categories})

@admin_router.post("/categories/new")
async def admin_create_category(
    request: Request,
    name: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    category_data = Category_sc(name=name)
    await _create_new_category(category_data, db)
    return RedirectResponse(url="/admin/categories", status_code=303)

@admin_router.get("/categories/{category_id}/delete")
async def admin_delete_category(request: Request, category_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await _delete_category(category_id, db)
        return RedirectResponse(url="/admin/categories", status_code=303)
    except HTTPException as e:
        # Если категория не может быть удалена (например, есть связанные товары)
        result = await db.execute(select(Categories))
        categories = result.scalars().all()
        return templates.TemplateResponse("admin/categories.html", {
            "request": request, 
            "categories": categories,
            "error": f"Ошибка при удалении категории: {e.detail}"
        })


    