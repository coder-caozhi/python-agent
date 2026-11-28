import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

# 0. 加载环境信息
load_dotenv(override=True)

# 使用deepseek-v4-flash解析一首诗
# 使用qwen3.7-max解析一首诗
# 使用glm对以上两个模型的解析结果进行对比和评价

# 1. 初始化三个模型
llm_deepseek = ChatOpenAI(model="deepseek-v4-flash")
llm_qwen = ChatOpenAI(model="qwen3.7-max", api_key=os.getenv("BAILIAN_API_KEY"), base_url=os.getenv("BAILIAN_BASE_URL"))
llm_glm = ChatOpenAI(model="glm-5.2", api_key=os.getenv("BAILIAN_API_KEY"), base_url=os.getenv("BAILIAN_BASE_URL"))

# 2 初始化结果解析器
parser = StrOutputParser()

# 3. 初始化提示词信息
prompt1 = PromptTemplate.from_template("对这首诗进行赏析:{poem}")
prompt2 = PromptTemplate.from_template("对这首诗进行赏析:{poem}")
prompt3 = PromptTemplate.from_template("对于以下两种赏析结果，进行总结。第一种:{result_deepseek}。第二种:{result_qwen}")

# 4. 编排三个链式流程
chain1 = prompt1 | llm_deepseek | parser
chain2 = prompt2 | llm_qwen | parser
chain3 = prompt3 | llm_glm | parser

# 5. 编排流程
chains = {
    "result_deepseek": chain1,
    "result_qwen": chain2
} | chain3


# 5. 执行
poem = "白日依山，黄河入海，世间万物，皆有裂痕。"
result = chains.invoke({"poem": poem})

# 6. 输出结果
print(result)
