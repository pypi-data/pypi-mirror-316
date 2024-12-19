from sqlalchemy.orm import Query

from src.config import settings


def paginate(stmt: Query, params: dict) -> dict:
    page = params.get('page', 1)
    size = params.get('size', settings.PAGINATION_SIZE)
    offset = size * (page - 1)
    total = stmt.count()
    results = stmt.offset(offset).limit(size).all()

    return {
        "results": results,
        "page": page,
        "size": size,
        "total": total,
    }
     