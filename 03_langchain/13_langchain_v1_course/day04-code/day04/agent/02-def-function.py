# ===== 第2步：定义工具的实际执行逻辑 =====
from dotenv import load_dotenv
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAI

load_dotenv(override=True)
client = OpenAI()

# 1. 定义一个工具。
# 如果不定义 description 自动读取 docString
@tool(description="获取指定城市在指定日期的天气")
def get_weather(city, date):
    """
    获取指定城市在指定日期的天气
    :param city:  城市名称，如"北京"、"上海"
    :param date:  日期，格式为YYYY-MM-DD
    :return: 天气信息
    """

    print("工具被调用。。。。。。。。。。。。。。")
    return f"{city} 在 {date} 天气晴朗，适合爬山。"

# result = get_weather.invoke({"city": "北京", "date": "2026-07-25"})
# print(result)

# 2. 声明一个模型客户端对象
llm = ChatOpenAI(model="deepseek-v4-pro")

# 2.5 将工具绑定到模型
tools = [get_weather]
llm = llm.bind_tools(tools)

# 3. 组装消息
messages = [
    HumanMessage(content="获取北京2026-07-25日的天气情况")
]

# 4. 模型调用
result = llm.invoke(messages)

# 封装最新的消息列表
messages.append(result)

tool_call = result.tool_calls[0]
args = tool_call['args']

# 调用工具
tool_call_result = get_weather.invoke(args)
id = tool_call['id']

# 组织工具调用的结果
messages.append(ToolMessage(content=tool_call_result, tool_call_id=id))

# 将工具调用的结果和之前所有的信息一起传递给模型
result = llm.invoke(messages)

print(result)

