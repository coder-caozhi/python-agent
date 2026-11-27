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
# 2.1 参数类型 ： 字符串
# res = model.invoke(input="你好")

# 2.2 参数类型： 列表
# messages = [
#     SystemMessage(content="你是一个脱口秀演员"),
#     HumanMessage(content="你今天过得怎么样")]
# res = model.invoke(input=messages)

# 2.3 参数类型：元组
# messages = [
#     ("system", "你是一个翻译"),
#     ("human", "翻译一下吴彦祖真帅")
# ]
# res = model.invoke(input=messages)

# 2.4 参数类型：字典
messages = [
    {"role": "system", "content": "你是一个厨师"},
    {"role": "human", "content": "翻译一下吴彦祖真帅"}
]
res = model.invoke(input=messages)


# 3. 输出结果
print(res.content)
