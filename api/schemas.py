from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator


class ProductCreate(BaseModel):
    """Схема, по которой мы добавляем новый продукт в БД"""
    name:str
    price:float
    quantity:int
    category:str


class ProductUpdate(BaseModel):
    """Схема, по которой мы обновляем продукт в БД"""
    name:str|None = None
    price:float|None = None
    quantity:int|None = None
    category:str|None = None


class ProductFilter(BaseModel):
    """Схема, по которой мы фильтруем продукты"""
    name:str = ""
    quantity_gt:int = 0
    quantity_lt:int = 100
    price_gt:int = 0
    price_lt:int = 100
    category:str = ""


class ProductDB(BaseModel):
    """Схема, по которой мы получаем ответ от БД"""
    id:int
    name:str
    price:float
    quantity:int
    category:Any
    category_id:int
    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)
    @field_validator("category")
    def cat_validator(cls,val):
        return val.name
    
class CategoryDB(BaseModel):
    """Схема, по которой мы получаем ответ от БД (категория)"""
    id:int
    name:str
    model_config = ConfigDict(from_attributes=True)