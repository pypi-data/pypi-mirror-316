from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.MYSQL_USER}:{quote(settings.MYSQL_PWD)}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=500,  # 连接池中的最大连接数
    max_overflow=50,  # 超出连接池大小时可以创建的额外连接数
    pool_pre_ping=True,  # 在每个连接上执行空语句以检测连接的有效性
    pool_recycle=3600,  # 在连接在连接池中超时之前的秒数
    pool_timeout=30,  # 从池中获取连接的超时时间，以秒为单位
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
