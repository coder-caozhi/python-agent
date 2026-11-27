import asyncio

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

# 0. 加载配置
load_dotenv(override=True)

# 1. 初始化客户端
model = init_chat_model(
    "openai:deepseek-v4-flash"
)

# 2. 调用模型
# 2.1 非流式输出
# res = model.invoke(input="你好")

res = model.stream(input="你好,请说五百个字的内容")


# 3. 返回结果
for r in res:
    print(r.content, end="")



