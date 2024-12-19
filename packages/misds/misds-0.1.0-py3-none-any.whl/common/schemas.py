from datetime import datetime
from typing import Any, List
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict
from src.core.database import SessionLocal

def convert_datetime_to_gmt(dt: datetime) -> str:
    if dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%d %H:%M:%S")


class CustomModel(BaseModel):
    
    
    model_config = ConfigDict(
        json_encoders={
            datetime: convert_datetime_to_gmt
        },
        populate_by_name=True
    )

    @property
    def db(self):
        return SessionLocal()
    
    def __del__(self):
        self.db.close()
        

class BaseResponseSchema(CustomModel):
    code: int = 200 # 状态码 200 成功 400及以上 失败
    msg: str = "success" # 状态信息
    data: Any # 返回数据


class PaginationSchema(CustomModel):
    results: List[Any] = [] # 返回数据列表
    page: int # 当前页码
    size: int # 每页数量
    total: int # 总数量
