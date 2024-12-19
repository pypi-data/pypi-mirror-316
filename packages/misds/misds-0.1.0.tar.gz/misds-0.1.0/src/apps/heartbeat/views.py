from fastapi import APIRouter

from src.common.logger import logger
from src.common.response import R

heartbeat_router = APIRouter()


@heartbeat_router.get("", summary="心跳检测")
def heartbeat():
    logger.info("heartbeat ！！!")
    return R.ok()
