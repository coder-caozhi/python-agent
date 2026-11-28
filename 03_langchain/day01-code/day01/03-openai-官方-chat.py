# 使用openai规范调用deepseek
import logging
import os

from openai import OpenAI
from dotenv import load_dotenv


logging.basicConfig(level=logging.WARNING)


# 0. 加载.env
load_dotenv(override=True)

# 1. 模型调用的客户端对象（client）
# client = OpenAI()  # 默认读取了环境变量中的OPENAI_API_KEY 和 OPENAI_BASE_URL
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

# 2. 模型调用
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {
            "role": "user",
            "content": "写一个关于独角兽的单句睡前小故事。"
        }
    ]
)

# 3. 解析输出
print(response)
print(response.choices[0].message.content)
