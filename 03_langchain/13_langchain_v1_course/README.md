# 13 新版 LangChain 课程

| 课次 | 学习内容 |
| --- | --- |
| [Day 01](day01-code/day01/) | 环境变量、模型接入、参数、同步与异步、流式与批量调用、提示词模板 |
| [Day 02](day02-code/day02/) | LCEL、结构化输出、Ollama、Markdown 和 Word 加载、MinerU 解析 PDF |
| [Day 03](day03-code/day03/rag/) | 文档切分、BGE 嵌入、Milvus 集合与数据写入 |
| [Day 04](day04-code/day04/) | 函数调用、工具参数、Agent 与会话隔离、Milvus 查询 |

Day 02 附带的 Day 01 版本用于对照课次，主线从 Day 01 入门。模型脚本按实际供应商配置所在课次的 `.env`。Day 01 和 Day 02 有各自的 `pyproject.toml` 和锁文件，可进入对应目录执行 `uv sync --locked` 复现课程环境。其他课次通常从脚本所在目录运行，使用根目录解释器。

Day 02 和 Day 03 共用 [文档样例](day03-code/assets/)。本地嵌入练习需要把已有 BGE 权重放到 `day03-code/assets/models/`，模型目录名见各脚本。原始权重保存在 `D:\python\python_grammar\05_langchain_11\day03-code\assets\models`。BGE、Milvus、MinerU、Ollama、Tavily 等练习需要对应的 Python 扩展、服务或密钥。
