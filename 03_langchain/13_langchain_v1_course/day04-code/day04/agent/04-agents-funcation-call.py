from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.agents import create_agent
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

# 1. 定义工具的参数
class GetWeatherArgs(BaseModel):
    """天气查询参数"""
    city: str = Field(description="城市名称，如'北京'、'上海'")
    date: str = Field(description="查询日期，格式为YYYY-MM-DD")


# 2. 定义一个工具。
# 如果不定义 description 自动读取 docString
@tool(description="获取指定城市在指定日期的天气", args_schema=GetWeatherArgs)
def get_weather(city, date):

    print("工具被调用。。。。。。。。。。。。。。")
    return f"{city} 在 {date} 天气晴朗，适合爬山。"

# 3. 初始化模型对象

llm = ChatOpenAI(
    model="deepseek-v4-pro"
)

# 4.初始化TavilySearch工具
search = TavilySearch(max_results=5)
tools = [get_weather, search]

# 5. 创建Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个智能助手，请根据用户的需求调用合适的工具来帮助他们。"
)

# # 6. 启动agent
# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "今天北京的天气如何"}]}
# )
#
# # 7. 获取最终的回复
# print(result)

for i, step in enumerate(agent.stream(
    # {"messages": [{"role": "user", "content": "今天北京的天气如何"}]}
    {"messages": [{"role": "user", "content": "今天的金价是多少"}]}
), start=1):
    print(f"======第 {i} 步==========")
    print(step, end="\n\n")