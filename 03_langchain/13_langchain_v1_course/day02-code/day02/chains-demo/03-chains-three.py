from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

# 0. 加载环境信息
load_dotenv(override=True)

# 1. 初始化模型调用客户端
llm = ChatOpenAI(model="deepseek-v4-flash")

# 2 初始化结果解析器
parser = StrOutputParser()

# 3. 初始化提示词信息
prompt1 = PromptTemplate.from_template("把这个句子翻译成英文:{topic}")
prompt2 = PromptTemplate.from_template("把这个句子翻译成韩文:{topic}")

# 4. 并编排流程
chain1 = prompt1 | llm | parser
chain2 = prompt2 | llm | parser

# 5. 创建并行链
chains = RunnableParallel(
    en=chain1,
    ko=chain2
)

# 5. 执行
result = chains.invoke({"topic": "我爱你"})

# 6. 输出结果
print(result["en"])
print(result["ko"])
