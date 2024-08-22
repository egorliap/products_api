import json
from typing import Annotated
from fastapi import APIRouter, Depends, Response

from .schemas import ProductCreate, ProductFilter, ProductUpdate
from .db import ProductOrm


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
async def get_products():
    prods = await ProductOrm.get_products()
    res = [x.model_dump() for x in prods]
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":True,
                            "message":f"Products found",
                            "products":res}
                            ),
                    media_type="application/json")

@router.get("/filter")
async def get_products_filter(filter: Annotated[ProductFilter,Depends()]):
    prods = await ProductOrm.get_products_filtered(filter)
    res = [x.model_dump() for x in prods]
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":True,
                            "message":f"Products found with your filter",
                            "products":res}
                            ),
                    media_type="application/json")

@router.get("/categories")
async def get_categories():
    cats = await ProductOrm.get_categories()
    res = [x.model_dump() for x in cats]
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":True,
                            "message":f"Categories found",
                            "categories":res}
                            ),
                    media_type="application/json")

@router.get("/categories/{category_id}")
async def get_category_by_id(category_id:int):
    cats = await ProductOrm.get_category_by_id(category_id)
    res = [x.model_dump() for x in cats]
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":True,
                            "message":f"Category with {category_id=} found",
                            "products":res}
                            ),
                    media_type="application/json")

@router.post("/")
async def create_product(product: Annotated[ProductCreate,Depends()]):
    res = await ProductOrm.add_product(product)
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":"true",
                            "message":f"New product is added with id of {res}"}
                            ),
                    media_type="application/json")
    
@router.get("/{product_id}")
async def get_product_by_id(product_id:int):
    prod = await ProductOrm.get_product_by_id(product_id)
    if not prod:
        return Response(status_code=404,
                        content=json.dumps(
                            {"success":False,
                            "message":f"Product with {product_id=} is not found",
                            "product":None}
                            ),
                        media_type="application/json")
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":True,
                            "message":f"Product with {product_id=} is found",
                            "product":prod.model_dump()}
                            ),
                    media_type="application/json")
    
@router.put("/{product_id}")
async def update_product(product_id:int, product: Annotated[ProductUpdate,Depends()] = ProductUpdate()):
    res = await ProductOrm.update_product(product_id,product)
    if(not res):
        return Response(status_code=404,
                        content=json.dumps(
                                {"success":False,
                                "message":f"Product with {product_id=} is not found"}
                                ),
                        media_type="application/json")
    else:
        return Response(status_code=200,
                        content=json.dumps(
                                {"success":True,
                                "message":f"Product with {product_id=} is updated"}
                                ),
                        media_type="application/json")

@router.delete("/{product_id}")
async def delete_product(product_id:int):
    await ProductOrm.delete_product(product_id)
    return Response(status_code=200,
                    content=json.dumps(
                                    {"success":True,
                                    "message":f"Product with {product_id=} is deleted"}
                                    ),
                    media_type="application/json")
    
