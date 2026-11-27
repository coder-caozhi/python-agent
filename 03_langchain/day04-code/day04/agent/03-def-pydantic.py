from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GetWeatherArgs(BaseModel):
    """天气查询参数"""
    city: str = Field(description="城市名称，如'北京'、'上海'")
    date: str = Field(description="查询日期，格式为YYYY-MM-DD")


# 1. 定义一个工具。
# 如果不定义 description 自动读取 docString
@tool(description="获取指定城市在指定日期的天气", args_schema=GetWeatherArgs)
def get_weather(city, date):

    print("工具被调用。。。。。。。。。。。。。。")
    return f"{city} 在 {date} 天气晴朗，适合爬山。"


result = get_weather.invoke({"city": "北京", "date": "2026-07-25"})
print(result)