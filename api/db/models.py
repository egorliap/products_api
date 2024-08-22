from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Category(Base):
    __tablename__ = "categories"
    id:Mapped[int] = mapped_column(primary_key=True, unique=True,autoincrement=True)
    name:Mapped[str]
    products: Mapped[List["Product"]] = relationship(back_populates="category")
    

class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True, unique=True,autoincrement=True)
    name:Mapped[str]
    price:Mapped[float]
    quantity:Mapped[int]
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
    