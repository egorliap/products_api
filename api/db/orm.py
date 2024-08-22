from typing import List
from sqlalchemy import delete, select, update
from sqlalchemy.orm import joinedload

from .models import Category, Product
from .base import session_factory
from api.schemas import CategoryDB, ProductCreate, ProductDB, ProductFilter, ProductUpdate


class ProductOrm:
    @classmethod
    async def get_product_by_id(cls, id:int)-> ProductDB|None:
        async with session_factory() as session:
            q = select(Product).filter(
                Product.id == id
            )
            res = await session.execute(q)
            scalar = res.scalars().one_or_none()
            if(scalar):
                return ProductDB.model_validate(scalar)
            else:
                return None
    
    
    @classmethod
    async def get_products(cls, limit: int=20, offset: int=1)-> List[ProductDB|None]:
        async with session_factory() as session:
            q = select(Product).limit(limit).offset(limit*(offset-1))
            res = await session.execute(q)
            return [ProductDB.model_validate(prod) for prod in res.scalars().all()]
    
    
    @classmethod
    async def get_products_filtered(cls, f:ProductFilter):
        async with session_factory() as session:
            q = select(Product)\
                .filter(
                Product.name.like("{}%".format(f.name)),
                Product.price <= f.price_lt,
                Product.price >= f.price_gt,
                Product.quantity <= f.quantity_lt,
                Product.quantity >= f.quantity_gt
                )\
                .options(joinedload(Product.category)\
                .load_only(Category.name))\
                    .filter(Category.name.like("{}%".format(f.category)))
                    
            res = await session.execute(q)
            
            return [ProductDB.model_validate(prod) for prod in res.scalars().all()]
    
    @classmethod
    async def get_categories(cls):
        async with session_factory() as session:
            q = select(Category)
            res = await session.execute(q)
            return [CategoryDB.model_validate(prod) for prod in res.scalars().all()]
    
    @classmethod
    async def get_category_by_id(cls, id:int):
        async with session_factory() as session:
            q = select(Product)\
                .options(joinedload(Product.category))\
                    .filter(Category.id == id)
            res = await session.execute(q)
            return [ProductDB.model_validate(prod) for prod in res.scalars().all()]
    
    @classmethod
    async def add_product(cls, product:ProductCreate)->int:
        async with session_factory() as session:  
            q = select(Category).filter(Category.name == product.category)
            res = await session.execute(q)
            res = res.scalar()
            if(not res):
                new_cat = Category(name=product.category)
                session.add(new_cat)
                await session.flush()
                await session.commit()
                await session.refresh(new_cat)
                cat_id = new_cat.id
            else:
                cat_id = res.id
            new_product = Product(name=product.name,
                                  price=product.price,
                                  quantity=product.quantity,
                                  category_id = cat_id)         
            session.add(new_product)
            await session.flush()
            await session.commit()
            await session.refresh(new_product)
            return new_product.id
    
    @classmethod
    async def update_product(cls,id:int,product:ProductUpdate)-> bool:
        async with session_factory() as session:
            q = select(Category).filter(Category.name == product.category)
            res = await session.execute(q)
            res = res.scalar()
            if(not res):
                new_cat = Category(name=product.category)
                session.add(new_cat)
                await session.flush()
                await session.commit()
                await session.refresh(new_cat)
                cat_id = new_cat.id
            else:
                cat_id = res.id
                
            q = select(Product).filter(Product.id == id)
            res = await session.execute(q)
            res = res.scalar()
            
            
            if(res):
                for key,value in product.model_dump().items():
                    if(value != None):
                        if(key == "category"):
                            setattr(res,"category_id",cat_id)
                            continue
                        setattr(res,key,value)
                
                await session.commit()
                return True
            return False
            
            
    @classmethod
    async def delete_product(cls,id:int)-> None:
        async with session_factory() as session:
            stmt = delete(Product).filter(Product.id == id)
            await session.execute(stmt)
            await session.commit()
            