# 0. 加载 .env
from typing import List

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv(override=True)

# 1. 定义要输出的json的格式
class Star(BaseModel):
    name: str
    age: int

class StarList(BaseModel):
    stars: List[Star]

# 2. 定义 json输出解析器
json_parser = JsonOutputParser(pydantic_object=StarList)
# 3. 生成json提示词模板：要求模型返回json信息
json_template = json_parser.get_format_instructions()
print(json_template)

# 4. 初始化提示词信息
messages = [
    {"role": "system", "content": json_template},
    {"role": "user", "content": "请帮我列出一些著名的足球明星"}
]

# 5. 初始化模型调用客户端
llm = ChatOpenAI(model="deepseek-v4-flash")

# 6. 调用模型
res = llm.invoke(input = messages)

# 7. 打印结果
print(type(res))
content = res.content
result = json_parser.parse(content)

# result['starts']
result.get("stars")

names = [star["name"] for star in result.get("stars")]

print(names)
