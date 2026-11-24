import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

# 加载配置
load_dotenv(override=True)

# 1. 初始化客户端
# 可以初始化所有的模型
model_1 = init_chat_model(
    "openai:deepseek-v4-flash",
    # base_url=os.getenv("OPENAI_BASE_URL"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    # temperature=0.5,
    # timeout=300,
    # max_tokens=25000,
)
model_2 = init_chat_model(
    model = "deepseek-v4-flash",
    model_provider="openai"
    # base_url=os.getenv("OPENAI_BASE_URL"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    # temperature=0.5,
    # timeout=300,
    # max_tokens=25000,
)

# 只初始化兼容openai标准的模型
model_3 = ChatOpenAI(model = "deepseek-v4-flash")

# 2. 调用模型
res = model_3.invoke(input="你好")

# 3. 输出结果
print(res.content)