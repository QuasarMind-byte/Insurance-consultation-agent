from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.infra.database import check_database, close_database
from app.modules.product.router import  router as product_router

from app.modules.chat_thread.router import router as chat_thread_router

configure_logging(settings.logging.level)
logger = get_logger(__name__)

# 生命周期管理
@asynccontextmanager
async def lifecycle_manager(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(f"Starting {settings.app.name}")
    try:
        await check_database()
        yield
    finally:
        logger.info(f"Stopping {settings.app.name}")
        await close_database()

app = FastAPI(
    title=settings.app.name,
    debug=settings.app.debug,
    lifespan=lifecycle_manager,
)
app.include_router(product_router)
app.include_router(chat_thread_router)

@app.get("/health", summary="Health Check")
async def health_check() -> dict[str, str]:
    logger.info("Health check", status="OK")
    return {"status": "OK"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=False,
    )
