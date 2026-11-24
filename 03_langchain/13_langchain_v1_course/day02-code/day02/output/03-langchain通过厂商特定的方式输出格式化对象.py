import os
from http.client import responses

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI
from pydantic import BaseModel

# 加载配置
load_dotenv(override=True)

# 定义要输出的格式
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# 初始化客户端：使用langchain中自带的openai协议的模型客户端创建方式
client = ChatOpenAI(
    model="gpt-5.1",
    # model = "deepseek-v4-flash",
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)

#组装消息对象
messages = [
    {"role": "system", "content": "请帮我从以下内容中提取相关信息"},
    {"role": "user", "content": "李明和韩梅梅星期五要去博物馆"}
]

# 调用模型
new_client = client.with_structured_output(schema=CalendarEvent)

# 直接返回结构化结果
res = new_client.invoke(input=messages)

print(res.name)
print(res.date)
print(res.participants)