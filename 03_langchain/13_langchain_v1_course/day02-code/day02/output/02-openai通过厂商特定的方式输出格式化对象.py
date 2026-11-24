import os
from http.client import responses

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# 加载配置
load_dotenv(override=True)

# 定义要输出的格式
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)
# client = OpenAI()

# 调用模型：使用传统的openai的模型client创建方式
response = client.responses.parse(
    model = "gpt-5.1",
    # 注意：此处使用deepseek无法解析结果
    # model = "deepseek-v4-flash",
    input = [
        {"role": "system", "content": "请帮我从以下内容中提取相关信息"},
        {"role": "user", "content": "李明和韩梅梅星期五要去博物馆"}
    ],
    text_format=CalendarEvent
)

# 获取响应结果对象
event = response.output_parsed
print(event)
