from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db
from apps.hives.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from apps.hives.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    return await product_service.create_product(
        db,
        payload,
    )


@router.get(
    "",
    response_model=list[ProductResponse],
)
async def list_products(
    db: AsyncSession = Depends(get_db),
):
    return await product_service.list_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_product(
        db,
        product_id,
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await product_service.update_product(
        db,
        product_id,
        payload,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    await product_service.delete_product(
        db,
        product_id,
    )
