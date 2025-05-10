from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Products, Categories
from typing import Optional, List
# from uuid import UUID


class ProductDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_product(
        self,
        category_id: int,
        title: str,
        description: str,
        price: float,
        main_photo: Optional[str] = None,
        additional_photos: Optional[List[str]] = None
    ) -> Products:
        new_product = Products(
            category_id=category_id,
            title=title,
            description=description,
            price=price,
            main_photo=main_photo,
            additional_photos=additional_photos
        )

        self.db_session.add(new_product)
        await self.db_session.flush()
        return new_product

    async def get_product_by_id(self, product_id: int) -> Optional[Products]:
        query = select(Products).where(Products.id == product_id)
        result = await self.db_session.execute(query)
        return result.unique().scalar_one_or_none()

    async def create_category(self, name: str) -> Categories:
        category = Categories(name=name)
        self.db_session.add(category)
        await self.db_session.flush()
        return category