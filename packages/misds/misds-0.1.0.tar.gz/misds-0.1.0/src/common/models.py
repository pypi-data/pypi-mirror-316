from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings


class Base(DeclarativeBase):
    @property
    def to_dict(self):
        data_dict = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name, None)
            if value:
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
            data_dict[c.name] = value
        return data_dict

    @declared_attr
    def __tablename__(cls):
        if cls.__tablename__:
            return f"{settings.MYSQL_TABLE_PREFIX}_{cls.__tablename__}"
        else:
            return f"{settings.MYSQL_TABLE_PREFIX}_{cls.__name__.lower()}"


# 脚手架基础模型
class AppBaseModel(Base):
    __abstract__ = True

    id = mapped_column(
        BigInteger, primary_key=True, index=True, autoincrement=True, comment="自增ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        insert_default=func.now(),
        comment="创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=0, server_default="0", comment="true->已删除，fasle->未删除"
    )
