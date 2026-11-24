# 使用openai规范调用deepseek
import os

from openai import OpenAI
from dotenv import load_dotenv

# 0. 加载.env
load_dotenv(override=True)

# 1. 模型调用的客户端对象（client）
# client = OpenAI()  # 默认读取了环境变量中的OPENAI_API_KEY 和 OPENAI_BASE_URL
client = OpenAI(
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)


# 2. 模型调用
response = client.chat.completions.create(
    # model="deepseek-v4-pro",
    model="gpt-5.6",
    messages=[
        {"role": "system", "content": "你是一个能提供帮助的态度友好的客户助手"},
        {"role": "user", "content": "尚硅谷最帅的男人是谁？"},
    ]
)

# 3. 解析输出
print(response.choices[0].message.content)
