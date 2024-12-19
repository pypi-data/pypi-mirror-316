
1. 数据库迁移

   ```
   alembic init alembic

   alembic revision --autogenerate -m "迁移版本信息"

   alembic upgrade head
   ```