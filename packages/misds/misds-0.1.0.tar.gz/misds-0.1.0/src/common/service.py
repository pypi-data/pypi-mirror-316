import datetime
from typing import Dict, List, Union

from pydantic import BaseModel
from sqlalchemy import and_, func, or_, text
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from src.common.logger import logger
from src.common.models import AppBaseModel
from src.common.pagination import paginate


class UniversalService:
    model: AppBaseModel = None
    search_fields = []

    # 校验
    @classmethod
    def verify_exist_by_id(cls, db: Session, id: int):
        data = db.query(cls.model).filter(cls.model.id == id).first()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{cls.model}_{id} 不存在",
            )
        return data

    # 通过字典新增
    @classmethod
    def create_signal_Model_from_dict(
        cls, db: Session, m: dict
    ) -> Union[None, BaseModel] | str:
        db_model = cls.model(**m)

        try:
            db.add(db_model)
            db.commit()
            db.refresh(db_model)
        except Exception as e:
            logger.error(f"[create] {cls}, {e}")
            db.rollback()
            return None

        return db_model

    # 创建单个对象
    @classmethod
    def create_signal_Model(
        cls, db: Session, m: BaseModel
    ) -> Union[None, BaseModel] | str:
        db_model = cls.model(**m.model_dump())
        try:
            db.add(db_model)
            db.commit()
            db.refresh(db_model)
        except Exception as e:
            logger.error(f"[create] {cls}, {e}")
            db.rollback()
            return None

        return db_model

    # 创建多个对象
    @classmethod
    def create_Model_bulk(
        cls, db: Session, objects: list[BaseModel]
    ) -> list[int] | str:
        model_objects = [cls.model(**m.model_dump()) for m in objects]
        try:
            db.add_all(model_objects)
            db.commit()
        except Exception as e:
            logger.error(f"[create] {cls}, {e}")
            db.rollback()
            return []

        return [obj.id for obj in model_objects]

    # 更新对象
    @classmethod
    def update_Model(cls, db: Session, form_data: BaseModel, id: int):
        update_line = (
            db.query(cls.model)
            .filter_by(id=id)
            .update(form_data.model_dump(exclude_unset=True))
        )
        try:
            db.commit()
        except Exception as e:
            logger.error(f"[update] {cls}, {e}")
            db.rollback()
            return -1

        return update_line

    # 更新多个对象
    @classmethod
    def update_Model_bulk(cls, db: Session, objects: list[BaseModel]):
        for form_data in objects:
            db.query(cls.model).filter(cls.model.id == form_data.id).update(
                form_data.model_dump(exclude_unset=True), synchronize_session="fetch"
            )
        try:
            db.commit()
        except Exception as e:
            logger.error(f"[update] {cls}, {e}")
            db.rollback()
            return []

        return [obj.id for obj in objects]

    # 通过搜索条件更新
    @classmethod
    def update_Model_by_filter(
        cls, db: Session, filters: Union[list | dict], update_info: dict
    ) -> int | str:
        if isinstance(filters, list):
            update_line = (
                db.query(cls.model)
                .filter(*filters)
                .update(update_info, synchronize_session="fetch")
            )
        else:
            update_line = (
                db.query(cls.model)
                .filter_by(**filters)
                .update(update_info, synchronize_session="fetch")
            )

        try:
            db.commit()
        except Exception as e:
            logger.error(f"[update] {cls}, {e}")
            db.rollback()
            return -1

        return update_line

    @classmethod
    def update_Model_status(cls, db: Session, ids: Union[int, list[int]], status: int):
        id_list = [ids] if type(ids) == int else ids
        update_line = (
            db.query(cls.model)
            .filter(cls.model.id.in_(id_list))
            .update({"status": status})
        )

        try:
            db.commit()
        except Exception as e:
            logger.error(f"[update] {cls}, {e}")
            db.rollback()
            return -1

        return update_line

    @classmethod
    def update_Model_deleted(
        cls, db: Session, ids: Union[int, list[int]], deleted: bool = True
    ):
        id_list = [ids] if type(ids) == int else ids
        update_line = (
            db.query(cls.model)
            .filter(cls.model.id.in_(id_list))
            .update({"is_deleted": deleted})
        )

        try:
            db.commit()
        except Exception as e:
            logger.error(f"[update] {cls}, {e}")
            db.rollback()
            return -1

        return update_line

    # 查
    @classmethod
    def get_Model_info_by_id(cls, db: Session, id: int):
        return db.query(cls.model).filter(cls.model.id == id).first()

    @classmethod
    def get_Model_info_by_id_bulk(cls, db: Session, idList: list[int]):
        return db.query(cls.model).filter(cls.model.id.in_(idList)).all()

    @classmethod
    def get_Model_info_all(cls, db: Session):
        return db.query(cls.model).filter().all()

    @classmethod
    def get_Model_info_by_filter(cls, db: Session, filter: dict):
        return db.query(cls.model).filter_by(**filter).first()

    @classmethod
    def get_Model_info_all_by_filter(cls, db: Session, filter: dict):
        return db.query(cls.model).filter_by(**filter).all()

    @classmethod
    def get_count_all_by_filter(cls, db: Session, filters: List):
        return db.query(func.count(cls.model.id)).filter(*filters).scalar()

    @classmethod
    def find_by_pagination_filter_by(
        cls, db: Session, filter: dict, pagenum: int, pagesize: int
    ):
        result = (
            db.query(cls.model)
            .filter_by(**filter)
            .order_by(cls.model.id.desc())
            .limit(pagesize)
            .offset((pagenum - 1) * pagesize)
            .all()
        )
        return result

    @classmethod
    def find_by_pagination(
        cls, db: Session, filters: list, pagenum: int, pagesize: int
    ):
        result = (
            db.query(cls.model)
            .filter(*filters)
            .order_by(cls.model.id.desc())
            .limit(pagesize)
            .offset((pagenum - 1) * pagesize)
            .all()
        )
        return result

    @classmethod
    def find_lastest(cls, db: Session):
        return db.query(cls.model).order_by(cls.model.id.desc()).first()

    # count
    @classmethod
    def get_Model_count_by_fliter(cls, db: Session, filters):
        return db.query(cls.model).filter_by(**filters).count()

    # 删
    @classmethod
    def delete_Model_line_by_id(cls, db: Session, id: int):
        num = db.query(cls.model).filter(cls.model.id == id).delete()
        try:
            db.commit()
        except Exception as e:
            logger.error(f"[delete] {cls}, {e}")
            db.rollback()
            return -1
        return num

    @classmethod
    def delete_Model_lines_by_filters(cls, db: Session, filters: Union[list | dict]):
        if type(filters) == list:
            num = db.query(cls.model).filter(*filters).delete()
        else:
            num = db.query(cls.model).filter_by(**filters).delete()

        try:
            db.commit()
        except Exception as e:
            logger.error(f"[delete] {cls}, {e}")
            db.rollback()
            return -1
        return num

    @classmethod
    def find_by_pagination_and_search(
        cls,
        db: Session,
        start: datetime.datetime | str | None = "",
        end: datetime.datetime | str | None = "",
        pagenum: int = 1,
        pagesize: int = 10,
        search: str = "",
    ):
        if not pagenum:
            pagenum = 1
        else:
            pagenum = int(pagenum)
        if not pagesize:
            pagesize = 10
        else:
            pagesize = int(pagesize)

        query = db.query(cls.model)
        if start and end:
            query = query.filter(
                and_(cls.model.created_at >= start, cls.model.created_at <= end)
            )
        if search:
            query = query.filter(
                or_(
                    cls.model.message.contains(search), cls.model.title.contains(search)
                )
            )

        result = (
            query.filter_by(is_deleted=False)
            .order_by(cls.model.created_at.desc())
            .limit(pagesize)
            .offset((pagenum - 1) * pagesize)
            .all()
        )

        return result

    @classmethod
    def find_by_search(cls, db: Session, search: str = "", search_fields: list = None):
        query = db.query(cls.model)
        if search:
            query = query.filter(
                or_(
                    text(f"cls.model.{search_field}.contains(search)")
                    for search_field in search_fields
                )
            )

        result = (
            query.filter_by(is_deleted=0).order_by(cls.model.created_at.desc()).all()
        )

        return result


class LogicService(UniversalService):
    search_fields = []

    @classmethod
    def contains_query(cls, query, *fields, **conditions):
        """
        创建一个包含查询，用于匹配指定字段和条件。

        :param fields: 字段列表，用于指定哪些字段进行查询。
        :param conditions: 条件字典，键为字段名称，值为要匹配的值。
        :return: 查询对象

        : example:
        contains_query('username', 'email'), username='john', email='john@example.com'
        """

        # 构建查询条件
        for field, value in conditions.items():
            if field not in fields:
                continue
            query = query.where(cls.model.c[field].contains(value))

        return query

    @classmethod
    def create_signal_Model(cls, db: Session, m):
        db_model = cls.model(**m.model_dump())
        try:
            db.add(db_model)
            db.commit()
            db.refresh(db_model)
        except Exception as e:
            logger.error(f"[create] {cls}, {e}")
            db.rollback()
            return None

        return db_model

    # 校验
    @classmethod
    def verify_exist_by_id(cls, db: Session, id: int):
        data = (
            db.query(cls.model)
            .filter(cls.model.id == id, cls.model.is_deleted == 0)
            .first()
        )
        return data if data else None

    # 查
    @classmethod
    def get_Model_info_by_id(cls, db: Session, id: int):
        return (
            db.query(cls.model)
            .filter(cls.model.id == id, cls.model.is_deleted == 0)
            .first()
        )

    @classmethod
    def get_Model_info_by_id_bulk(cls, db: Session, idList: list[int]):
        return (
            db.query(cls.model)
            .filter(cls.model.id.in_(idList), cls.model.is_deleted == 0)
            .all()
        )

    @classmethod
    def get_Model_info_all(cls, db: Session):
        return db.query(cls.model).filter(cls.model.is_deleted == 0).all()

    @classmethod
    def get_Model_info_by_filter(cls, db: Session, filter: dict):
        return (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0)
            .filter_by(**filter)
            .first()
        )

    @classmethod
    def get_Model_info_by_in_filter(cls, db: Session, field: str, values: list):
        return (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0, getattr(cls.model, field).in_(values))
            .all()
        )

    @classmethod
    def get_Model_info_by_in_filters(
        cls, db: Session, filter: dict, field: str, values: list
    ):
        return (
            db.query(cls.model)
            .filter_by(**filter)
            .filter(cls.model.is_deleted == 0, getattr(cls.model, field).in_(values))
            .all()
        )

    @classmethod
    def get_Model_info_by_filter_ne_id(cls, db: Session, filter: dict):
        return (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0, cls.model.id != filter.pop("id"))
            .filter_by(**filter)
            .first()
        )

    @classmethod
    def get_Model_info_all_by_filter(cls, db: Session, filter: dict):
        return (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0)
            .filter_by(**filter)
            .all()
        )

    @classmethod
    def find_by_pagination(cls, db: Session, filters, pagenum, pagesize):
        result = (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0)
            .filter(*filters)
            .order_by(cls.model.id.desc())
            .limit(pagesize)
            .offset((pagenum - 1) * pagesize)
            .all()
        )
        return result

    # count
    @classmethod
    def get_Model_count_by_fliter(cls, db: Session, filters):
        return (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0)
            .filter_by(**filters)
            .count()
        )

    # 删
    @classmethod
    def delete_Model_line_by_id(cls, db: Session, id: int):
        num = (
            db.query(cls.model)
            .filter(cls.model.id == id, cls.model.is_deleted == 0)
            .delete()
        )
        try:
            db.commit()
        except Exception as e:
            logger.error(f"[delete] {cls}, {e}")
            db.rollback()
            return None
        return num

    @classmethod
    def delete_Model_lines_by_filters(cls, db: Session, filters):
        num = (
            db.query(cls.model)
            .filter(cls.model.is_deleted == 0)
            .filter(*filters)
            .delete()
        )
        try:
            db.commit()
        except Exception as e:
            logger.error(f"[delete] {cls}, {e}")
            db.rollback()
            return None
        return num

    @classmethod
    def find_by_pagination_and_search(
        cls,
        db: Session,
        page_params: dict,
        start: datetime.datetime | str | None = "",
        end: datetime.datetime | str | None = "",
        search: str = "",
    ):
        query = db.query(cls.model)
        if start and end:
            query = query.filter(
                and_(cls.model.created_at >= start, cls.model.created_at <= end)
            )
        if search and cls.search_fields:
            conditions = [
                getattr(cls.model, column).contains(search)
                for column in cls.search_fields
            ]
            query = query.filter(or_(*conditions))

        query_stmt = query.filter_by(is_deleted=False).order_by(text("-created_at"))
        return paginate(query_stmt, page_params)

    @classmethod
    def find_by_search(cls, db: Session, filters: dict = None, search: str = ""):
        query = db.query(cls.model)

        if search and cls.search_fields:
            conditions = [
                getattr(cls.model, column).contains(search)
                for column in cls.search_fields
            ]
            query = query.filter(or_(*conditions))

        if filters:
            query = query.filter_by(**filters)
        result = (
            query.filter_by(is_deleted=0).order_by(cls.model.created_at.desc()).all()
        )

        return result

    @classmethod
    def build_filter_conditions(cls, filters: Dict[str, str]) -> List:
        conditions = []
        for field, value in filters.items():
            if value is not None:
                condition = text(f"{field} = {value}")
                conditions.append(condition)
        return conditions
