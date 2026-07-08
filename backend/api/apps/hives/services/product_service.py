from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.hives.models import Product
from apps.hives.schemas import ProductCreate, ProductUpdate
from core.exceptions import NotFoundException


async def create_product(
    db: AsyncSession,
    payload: ProductCreate,
) -> Product:
    product = Product(
        **payload.model_dump(),
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


async def list_products(
    db: AsyncSession,
) -> list[Product]:
    result = await db.execute(
        select(Product).where(Product.is_active.is_(True)).order_by(Product.name)
    )

    return list(result.scalars().all())


async def get_product(
    db: AsyncSession,
    product_id: int,
) -> Product:
    product = await db.get(Product, product_id)

    if not product:
        raise NotFoundException("Product not found")

    return product


async def update_product(
    db: AsyncSession,
    product_id: int,
    payload: ProductUpdate,
) -> Product:
    product = await get_product(db, product_id)

    data = payload.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


async def delete_product(
    db: AsyncSession,
    product_id: int,
) -> None:
    product = await get_product(db, product_id)

    product.is_active = False

    await db.commit()
