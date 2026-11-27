import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 加载配置
load_dotenv(override=True)

# 1. 初始化客户端
model = init_chat_model(
    "openai:deepseek-v4-flash",
    # base_url=os.getenv("OPENAI_BASE_URL"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    # temperature=0.5,
    # timeout=300,
    # max_tokens=25000,
)
model = init_chat_model(
    model = "deepseek-v4-flash",
    model_provider="openai"
    # base_url=os.getenv("OPENAI_BASE_URL"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    # temperature=0.5,
    # timeout=300,
    # max_tokens=25000,
)

# 2. 调用模型
res = model.invoke(input="你好")

# 3. 输出结果
print(res.content)

# 总结：
# 1. load_dotenv(override=True) 加载 .env，文件中的同名配置会覆盖已有环境变量。
# 2. init_chat_model 可以用“提供商:模型名”或 model + model_provider 两种写法初始化聊天模型。
#    本例连续赋值两次，第二次会覆盖第一次；实际使用时选择一种写法即可。
# 3. model_provider="openai" 表示使用 OpenAI 兼容接口；调用其他服务时，
#    需要按服务商要求配置接口地址、API 密钥和模型名称。
# 4. temperature 控制输出的随机性，timeout 设置请求超时时间，max_tokens 限制生成的 token 数。
#    这些参数目前都被注释，实际调用时使用模型集成的默认配置。
# 5. invoke() 同步发送输入并返回消息对象；通过 res.content 获取回复内容。
