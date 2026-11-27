from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.modules.product.models import Product
from app.modules.product.schemas import ProductResponse
from app.modules.product.service import ProductService

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/products", tags=["products"])

# 如果接口较多，每个接口都手动创建比较麻烦，可以将获取service的代码抽取为函数，通过依赖注入来获取：
async def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(session)

"""
List products by category.
"""
@router.get("", response_model=list[ProductResponse])
async def list_products(category: str | None = None, service: ProductService = Depends(get_product_service)) -> list[Product]:

    return await service.list_products(category)


"""
List candidates for a given category and premium minimum.
- categories 没有默认值，因此至少要传一个险种；
- premium_min 必须大于 0，
- limit_per_category 限制在 1～10 之间，防止一次查询返回过多数据。
"""
@router.get("/candidates", response_model=list[ProductResponse])
async def list_candidates(
    categories: list[str] = Query(min_length=1),
    premium_min: Decimal | None = None,
    limit_per_category: int = 5,
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    return await service.list_candidates(
        categories=categories,
        premium_min=premium_min,
        limit_per_category=limit_per_category,
    )