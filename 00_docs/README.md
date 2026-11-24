# 项目结构与复习

| 原位置 | 新位置 |
| --- | --- |
| python_grammar 的 Python 基础和 FastAPI | [01_python_basics](../01_python_basics/README.md) 与 [02_fastapi](../02_fastapi/README.md) |
| python_grammar 的 LangChain 主题练习 | [03_langchain](../03_langchain/README.md) 的 01–12 章 |
| python_grammar 的 05_langchain_11 | [13_langchain_v1_course](../03_langchain/13_langchain_v1_course/README.md) |
| langgraph-demo | [04_langgraph](../04_langgraph/README.md) |
| deepagents-demo | [05_deepagents](../05_deepagents/README.md) |
| python_grammar 的五月课程与历史迁移资料 | [90_course_materials](../90_course_materials/README.md) 与 [历史文档](python_grammar_archive/README.md) |

## 把五个阶段串起来

1. 用 Python 函数处理一条输入。练习给参数和返回值加类型标注，用异常处理无效输入。
2. 用 FastAPI 把函数放到一个 POST 路由后。用 Pydantic 验证请求体，用测试客户端检查正常和错误响应。
3. 把函数注册为 LangChain 工具，先单独调用工具，再让 Agent 根据用户输入选择调用。
4. 用 LangGraph 把输入、检索和回答放进 State，给分支设置条件，观察检查点如何保存一次执行。
5. 用 Deep Agents 将检索、整理交给不同子代理。为会写入状态的工具加入人工审核，练习审核后恢复执行。

根目录的 `pyproject.toml` 与 `uv.lock` 管理主线环境，默认使用 Python 3.13。各阶段的 `.env.example` 是对应示例的配置模板。旧课次自带的依赖文件可用于复现当时的环境，模型权重和外部服务按示例单独配置。

新增章节沿用两位序号和主题名。课程原文件、素材和版本变体保留原名，方便与课件对照。
