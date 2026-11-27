# 使用openai规范调用deepseek
import os

from dotenv import load_dotenv
from openai import OpenAI

# 0. 加载.env
load_dotenv(override=True)

# 1. 模型调用的客户端对象（client）
# client = OpenAI()  # 默认读取了环境变量中的OPENAI_API_KEY 和 OPENAI_BASE_URL
client = OpenAI(
    api_key=os.getenv("BAILIAN_API_KEY"),
    base_url=os.getenv("BAILIAN_BASE_URL")
)

# 2. 模型调用
completion = client.chat.completions.create(
    model="qwen-vl-plus",
    # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}
                },
                {
                    "type": "text",
                    "text": "这是什么"
                },
            ]
        }
    ]
)

# 3. 解析输出
print(completion.model_dump_json())
