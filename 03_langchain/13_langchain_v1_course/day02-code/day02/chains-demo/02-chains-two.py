

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 0. 加载环境信息
load_dotenv(override=True)

# 1. 初始化提示词信息:并且调用invoke 方法渲染提示词
prompt_template = PromptTemplate.from_template("给我写一个关于{keyword}的信息")
# 2. 初始化模型调用客户端
llm = ChatOpenAI(model="deepseek-v4-flash")
# 3 初始化结果解析器
parser = StrOutputParser()


# 4. 编排流程
chains = prompt_template | llm | parser
str_result = chains.invoke({"keyword": "人工智能"})
print(str_result)
