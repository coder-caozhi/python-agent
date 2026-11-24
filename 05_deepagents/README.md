# 05 Deep Agents

先跑单 Agent，再练习委派任务、拦截工具调用和恢复执行。

| 主题 | 示例 |
| --- | --- |
| 调用与流式输出 | [invoke](base/01_deep_agents_hello_invoke.py) → [stream](base/02_deep_agents_hello_stream.py) |
| 子代理 | [字典声明](base/03_deep_agents_subagents_dict.py) → [封装 LangChain Agent](base/04_deep_agents_subagents_compiledsubagent_langchain.py) → [封装 LangGraph 图](base/05_deep_agents_subagents_compiledsubagent_langgraph.py) |
| 人工审核 | [批准和拒绝](base/06_deep_agents_hitl_approve_reject.py) → [修改参数](base/07_deep_agents_hitl_edit.py) |
| 文件、存储与会话状态 | [FilesystemBackend](base/deep_agent_10.py) → [StoreBackend](base/deep_agent_11.py) → [CompositeBackend](base/deep_agent_12.py) |
| 中间件和技能 | [工具拦截](base/deep_agent_13.py) → [工具日志](base/deep_agent_14.py) → [技能目录](base/deep_agent_15.py) |

参考 [课程笔记](notes/day01_deepagents基本概念和基础能力.md) 和 [原使用总结](base/DeepAgents使用总结.txt)。`base/deep_agent_01.py` 到 `base/deep_agent_15.py` 保留课堂练习。包含文件读写的示例会使用 `base/agent_workspace` 中的练习文件。

从仓库根目录复制配置模板，填入模型配置和联网工具所需的密钥，再运行示例。

```powershell
Copy-Item .\05_deepagents\.env.example .\05_deepagents\.env
uv run --locked --directory .\05_deepagents\base python .\01_deep_agents_hello_invoke.py
```

`LLM_MODEL` 对应编号示例，`LLM_QWEN_MAX` 用于部分课堂脚本。根据脚本使用的模型填写匹配的 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`。联网例子读取 `TAVILY_API_KEY`。
