from fastapi import APIRouter

from src.common.logger import logger
from src.common.response import R

excute_router = APIRouter()


@excute_router.post("", response_model="",summary="执行任务模块")
def excute():
    
    logger.info("excute ！！！")
    
    
    
    return R.ok()


class 