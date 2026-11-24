# python-agent

从 Python 基础到 AI Agent 的学习项目。按下面五个阶段练习，每个阶段都可以独立选读。

| 阶段 | 练习顺序 | 学完能做什么 |
| --- | --- | --- |
| [01 Python 基础](01_python_basics/README.md) | 语法 → 容器与函数 → 模块、类、异常 → 文件、生成器、异步 | 写出可独立运行的脚本，读懂后续示例的类型标注和异步调用 |
| [02 FastAPI](02_fastapi/README.md) | 路由与参数 → Pydantic → SQLAlchemy → 部门员工 CRUD | 接收、校验和持久化 HTTP 请求 |
| [03 LangChain](03_langchain/README.md) | 模型与提示词 → LCEL 与结构化输出 → 工具、记忆、RAG、Agent | 调用模型、检索资料并让 Agent 调用工具 |
| [04 LangGraph](04_langgraph/README.md) | 最小工作流 → State 与 Reducer → 节点与边 → Checkpointer 与中断 | 编排分支、循环和可恢复的工作流 |
| [05 Deep Agents](05_deepagents/README.md) | 调用与流式输出 → 子代理 → 人工审核 → 文件后端、技能和中间件 | 把复杂任务拆给子代理，并在指定工具执行前加入审核 |

## 开始运行

在 PowerShell 中进入项目根目录。

```powershell
cd D:\python\python-agent
uv sync --locked
uv run --locked python -m 04_langgraph.02_get_started.workflow_demo
```

这条工作流用本地函数模拟检索与汇总，无需 API 密钥。PyCharm 打开项目根目录，解释器选 `.venv\Scripts\python.exe`。普通练习用脚本所在目录作为工作目录，以便读取相邻文件。带模型、数据库或本地服务的练习按章节说明配置。

[目录来源、环境与复习顺序](00_docs/README.md) · [原始参考课件](90_course_materials/README.md)
