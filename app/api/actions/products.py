from fastapi import HTTPException, Body

from app.api.models import Product_sc, ProductUpdate_sc, Category_sc
from app.db.dals import ProductDAL

from sqlalchemy import select, delete, or_
from sqlalchemy.orm import selectinload

from app.db.models import Products, Categories, ProductPhoto


#CREATE
async def _create_new_product(body: Product_sc, session) -> Product_sc:
    async with session.begin():
        p_dal = ProductDAL(session)
        product = await p_dal.create_product(
            category_id=body.category_id,
            title=body.title,
            description=body.description,
            price=body.price,
            photos=body.photos,
        )
        # Подгружаем товар с фотографиями через selectinlop
        result = await session.execute(
            select(Products).options(selectinload(Products.photos)).where(Products.id == product.id)
        )
        product_with_photos = result.scalar_one()
        return Product_sc(
            category_id=product_with_photos.category_id,
            title=product_with_photos.title,
            description=product_with_photos.description,
            price=product_with_photos.price,
            photos=[photo.file_path for photo in product_with_photos.photos] if product_with_photos.photos else None
        )


async def _create_new_category(body: Category_sc, session)-> Category_sc:
    async with session.begin():
        p_dal = ProductDAL(session)
        existing = await session.execute(select(Categories).where(Categories.name == body.name))
        if existing.scalar():
            raise HTTPException(status_code=400, detail="Категория уже существует")
        category = await p_dal.create_category(name=body.name)
        return Category_sc(name=category.name)


###DELETE
async def _delete_category(category_id: int, session):
    async with session.begin():
        result = await session.execute(delete(Categories).where(Categories.id == category_id))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Категория не найдена")


async def _delete_product(product_id: int, session):
    async with session.begin():
        # Получаем объект объявления
        result = await session.execute(select(Products).where(Products.id == product_id))
        p = result.unique().scalar_one_or_none()

        if p is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

###GET
async def _get_product_by_id(product_id: int, session) -> Product_sc:
    async with session.begin():
        product_dal = ProductDAL(session)
        product = await product_dal.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        return Product_sc(
            id=product.id,
            category_id=product.category_id,
            title=product.title,
            description=product.description,
            price=product.price,
            photos=product.photos,
        )


 # отдаёт все товары
async def _get_all_products(session):
    async with session.begin():
        # product_dal = ProductDAL(session)
        result = await session.execute(select(Products))
        ps = result.unique().scalars().all()
        return [
            Product_sc(
                id=p.id,
                user_id=p.user_id,
                category_id=p.category_id,
                title=p.title,
                description=p.description,
                pdress=p.pdress,
                dormitory_id=p.dormitory_id,
                price=p.price,
                photos=[photo.file_path for photo in p.photos] if p.photos else None
            ) for p in ps
        ]

# отдаёт результаты поиска
async def _get_search_products(session, search_term: str | None = None):
    async with session.begin():
        stmt = select(Products).options(selectinload(Products.photos))

        if search_term:
            search_pattern = f"%{search_term}%"

            stmt = stmt.where(
                or_(
                    Products.title.ilike(search_pattern),
                    Products.description.ilike(search_pattern),
                )
            )

        stmt = stmt.order_by(Products.id.desc())
        result = await session.execute(stmt)
        products = result.unique().scalars().all()
        return [
            Product_sc(
                id=product.id,
                user_id=product.user_id,
                category_id=product.category_id,
                title=product.title,
                description=product.description,
                price=product.price,
                photos=[photo.file_path for photo in product.photos] if product.photos else None
            ) for product in products
        ]

###UPDATE
async def _update_product(product_id: int, session,  update: ProductUpdate_sc = Body(...)):
    async with session.begin():
        product_dal = ProductDAL(session)
        product = await product_dal.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Объявление не найдено")

        # обновление полей
        for field, value in update.dict(exclude_unset=True).items():
            if field == "photos":
                product.photos = [ProductPhoto(file_path=path) for path in value]
            else:
                setattr(product, field, value)

        await session.flush()

        return Product_sc(
            id=product.id,
            category_id=product.category_id,
            title=product.title,
            description=product.description,
            price=product.price,
            photos=[photo.file_path for photo in product.photos] if product.photos else None,
        )
