

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv(override=True)


# 创建checkpointer（内存存储，程序重启后数据会丢失）
# checkpointer = InMemorySaver()

# # ===== 1. 初始化LLM =====
llm = init_chat_model(model="deepseek-v4-pro", model_provider="openai")

# # 创建Agent时传入checkpointer
# agent = create_agent(
#     model=llm,
#     checkpointer=checkpointer,     # ← 就这一行
# )


res1 = llm.invoke("我叫张三")
print(res1)

res2 = llm.invoke("我叫李四？")
print(res2)

res3 = llm.invoke("我叫什么？")
print(res3)