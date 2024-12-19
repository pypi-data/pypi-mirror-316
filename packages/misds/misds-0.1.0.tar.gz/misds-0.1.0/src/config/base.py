import time
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
    )

    # 项目基础配置
    APP_DEBUG: bool = False
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "基于微服务的分布式任务调度框架系统"
    DESCRIPTION: str = ""
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    PORT: int = 9055
    API_PREFIX: str = "api"

    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # MySQL
    MYSQL_TABLE_PREFIX: str = "misds"  # 数据库表前缀
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PWD: str
    MYSQL_DB: str = "misds"

    # Redis
    REDIS_HOST: str = "192.168.101.159"
    REDIS_PORT: int = 31701
    REDIS_PASSWORD: str = "myredis"
    REDIS_DB: str = 0

    # 分页
    PAGINATION_SIZE: int = 10
    PAGINATION_MAX_SIZE: int = 50

    # 日志配置 10 ,20 ,30 ,40 50
    LOG_LEVEL: int = 10
    LOG_FILENAME: str = f"{time.strftime('%Y%m%d')}.log"
    LOG_FILEPATH: Path = Path(BASE_DIR, "logs")
    LOG_FORMAT: str = (
        "<green><b>{time:YYYY-MM-DD HH:mm:ss.SSS}</b></green> | "
        "<level>{level:8}</level> | "
        "<level>{traceid}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # nacos 配置
    NACOS_SERVER_ADDRESSES: str = "192.168.101.159:30511"
    # 命名空间（可选）
    NACOS_NAMESPACE: str = "public"
    # 服务名
    NACOS_SERVICE_NAME: str = "misds-client"
    # 分组（可选）
    NACOS_GROUP_NAME: str = "DEFAULT_GROUP"
    # 集群名（可选）
    NACOS_CLUSTER_NAME: str = "DEFAULT"

    NACOS_USER_NAME: str = "nacos"
    NACOS_PASSWORD: str = "nacos"
