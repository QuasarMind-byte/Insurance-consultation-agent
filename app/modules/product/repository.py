from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    """Find products by category."""
    async def find_by_category(self, category: str | None = None) -> list[Product]:
        conditions = [Product.status == "active"]
        if category:
            conditions.append(Product.category == category)

        Products = await self.session.scalars(
            select(Product)
            .where(*conditions)
            .order_by(Product.id.desc())
        )
        return Products.all()


    """Find limited products by category."""
    async def find_limited_by_category(
            self,
            category: str,
            premium_min: Decimal | None,
            limit: int,
    ) -> list[Product]:
        conditions = [
            Product.status == "active",
            Product.category == category,
        ]
        if premium_min is not None:
            conditions.append(Product.min_premium < premium_min)

        products = await self.session.scalars(
            select(Product)
            .where(*conditions)
            .order_by(
                Product.min_premium.asc().nullslast(),
                Product.id.asc(),
            )
            .limit(limit)
        )
        return products.all()
