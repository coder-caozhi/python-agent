

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 0. 加载环境信息
load_dotenv(override=True)

# 1. 初始化提示词信息:并且调用invoke 方法渲染提示词
prompt_template = PromptTemplate.from_template("给我写一个关于{keyword}的信息")
prompt = prompt_template.invoke({"keyword": "人工智能"})

# 2. 初始化模型调用客户端
llm = ChatOpenAI(model="deepseek-v4-flash")
# 3. 调用模型
result = llm.invoke(prompt)

# 4. 获取结果
parser = StrOutputParser()
str_result = parser.invoke(result)

print(str_result)