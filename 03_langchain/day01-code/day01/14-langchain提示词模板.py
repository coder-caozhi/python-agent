import asyncio

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# 0. 加载配置
load_dotenv(override=True)

# 1. 初始化客户端
model = init_chat_model(
    "openai:deepseek-v4-flash"
)

# 2. 组装messages
messages = [
    ("system", "你是一个{worker}"),  # 定义一个槽位（占位符）
    ("human", "我想咨询关于{query}的问题")
]

# messages_result = [
#     ("system", "你是一个经纪人"),  # 定义一个槽位（占位符）
#     ("human", "我想咨询关于男明星最帅的三位是谁的问题")
# ]

# 3. 创建提示词模板对象
cpt = ChatPromptTemplate.from_messages(messages=messages)
messages_result = cpt.invoke(input={"worker": "明星", "query": "男明星最帅的三位是谁"})

# 4. 调用模型
res = model.invoke(input=messages_result)

# 5. 返回结果
print(res.content)




