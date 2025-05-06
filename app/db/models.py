from sqlalchemy import Column, Integer, ForeignKey, String, Float
# from sqlalchemy.dialects.postgresql import UUID если буду делать сущность юзера
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # связи с категориями и фото
    category = relationship("Categories", back_populates="products")
    photos = relationship("ProductPhoto", back_populates="products", cascade="all, delete-orphan", lazy="joined")


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)

    # связь с товарами(Products)
    products = relationship("Products", back_populates="category")

class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    file_path = Column(String, nullable=False)

    products = relationship("Products", back_populates="photos")