import asyncio

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 0. 加载配置
load_dotenv(override=True)

# 1. 初始化客户端
model = init_chat_model(
    "openai:deepseek-v4-flash"
)

# 组装messages
messages = [
    [
        ("system", "你是一个大模型讲师"),
        ("human", "如何学习LangChain")
    ],
    [
        ("system", "你是一个大模型讲师"),
        ("human", "如何学习LangGraph")
    ]
]

# 3. 调用模型
# 通过线程池的方式提交
res = model.batch(inputs=messages)

# 4. 返回结果
for r in res:
    print(r.content)
    print("-" * 80)



