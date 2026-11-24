# 04 LangGraph

LangGraph 把工作流拆成共享状态、节点和边。先跑一遍固定图，再在节点中观察状态增量如何被合并。

| 顺序 | 示例 | 观察什么 |
| --- | --- | --- |
| 1 | [入门工作流](02_get_started/workflow_demo.py) | 两路检索并行执行后汇总 |
| 2 | [State](03-state/) | Dict、TypedDict、Pydantic 和 dataclass，各节点通过 Reducer 合并更新 |
| 3 | [节点](04-nodes/) | 参数、错误输出、缓存、重试、流式输出与中断 |
| 4 | [边](05-edge/) | 条件路由与循环上限 |
| 5 | [检查点](03-state/14_langgraph_checkpointer_demo.py) → [状态恢复](03-state/15_state_recovery_demo.py) → [历史查询](03-state/17_state_history_demo.py) | 用 thread_id 区分执行，用 checkpoint 查询或恢复状态 |

从仓库根目录运行模块，让共享的 `llm_config.py` 能正常导入。

```powershell
uv run --locked --directory .\04_langgraph python -m 02_get_started.workflow_demo
uv run --locked --directory .\04_langgraph python -m 05-edge.01_condition_edge
```

按同样方式运行 [模型流式输出](04-nodes/08_stream_demo.py) 等模型示例前，在本章由 `.env.example` 创建 `.env` 并填写供应商配置。模拟工作流、状态、条件边等本地示例可直接运行。
