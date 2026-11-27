from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
# 统一管理连接池

# 1.数据库连接地址
if not settings.database or not settings.database.url:
    raise RuntimeError("数据库连接地址不能为空")

DATABASE_URL = settings.database.url

# 2.创建异步数据库引擎
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=settings.database.echo,  # 是否打印SQL语句
    pool_size=settings.database.pool_size,  # 连接池中长期保留的连接数
    max_overflow=settings.database.max_overflow,  # 连接池满后，允许临时创建的额外连接数
    pool_recycle=settings.database.pool_recycle,  # 连接存活超过该时间后，在下次取出时重新创建
    pool_pre_ping=True,  # 从连接池取出连接时，先检查连接是否有效
)

# 3.创建异步会话工厂
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

# 4.获取异步 session 工厂
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise e

# 5.关闭连接池
async def close_database():
    await engine.dispose()
    logger.info("数据库连接池已关闭")

# 6.数据库健康检查
async def check_database() -> None:
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("数据库健康检查成功")


