from fastapi import Query

from src.config import settings
from src.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def page_params(
    page: int | None = Query(1, ge=1, description="页码"),
    size: int | None = Query(
        settings.PAGINATION_SIZE,
        gt=0,
        le=settings.PAGINATION_MAX_SIZE,
        description="每页的数量",
    ),
):
    if not page:
        page = 1
    if not size:
        size = settings.PAGINATION_SIZE
    return {"page": page, "size": size}
