from fastapi import APIRouter

from src.apps.excute.views import excute_router
from src.apps.heartbeat.views import heartbeat_router
from src.config import settings

if settings.API_PREFIX:
    url_prefix = f"/{settings.API_PREFIX}"
else:
    url_prefix = ""


router = APIRouter(prefix=url_prefix)


# 系统相关路由
router.include_router(excute_router, prefix="/excute", tags=["执行模块"])
router.include_router(heartbeat_router, prefix="/heartbeat", tags=["心跳检测模块"])
