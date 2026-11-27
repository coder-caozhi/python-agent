# 02 FastAPI

先用路由与参数练习理解请求如何进到 Python 函数，再连接数据库完成增删改查。

| 顺序 | 示例 | 观察什么 |
| --- | --- | --- |
| 1 | [路由与 ORM 课堂练习](01_routing_and_orm_practice/README.md) | 路径、查询参数、请求体和路由拆分 |
| 2 | [部门与员工 CRUD](02_department_employee_crud/README.md) | Pydantic 校验、SQLAlchemy Session、主外键关系、错误响应和接口测试 |

从项目根目录启动路由练习，无需先配置 MySQL。

```powershell
uv run --locked --directory .\02_fastapi\01_routing_and_orm_practice uvicorn main:app --reload --port 8002
```

启动后打开 [Swagger UI](http://127.0.0.1:8002/docs)，试一下 `GET /hello/{name}`，再对照 `main.py` 和 `routers/`。接下来按完整 CRUD 的说明配置 MySQL。课堂练习附带的测试来自早期 CRUD 示例，当前接口以完整 CRUD 目录的测试为准。
