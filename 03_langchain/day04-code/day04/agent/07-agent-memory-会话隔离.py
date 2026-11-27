import datetime

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv(override=True)

# 准备工具和模型
search = TavilySearch(max_results=5)
llm = init_chat_model(model="deepseek-v4-pro", model_provider="openai")

# 创建有记忆的Agent
checkpointer = InMemorySaver()

# 创建智能体
agent = create_agent(
    model=llm,
    tools=[search],
    checkpointer=checkpointer,
)

# ===== 第1次调用 =====
print("=== 第1次调用 ===")
for chunk in agent.stream(
    input={
        "messages": [
            {
                "role": "system",
                "content": f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            },
            {"role": "user", "content": "今天北京天气怎么样？"},
        ]
    },
    config={"configurable": {"thread_id": "abc123"}},
):
    print(chunk, end="\n\n")

# ===== 第2次调用（相同thread_id → 有记忆） =====
print("=== 第2次调用 ===")
for chunk in agent.stream(
    input={
        "messages": [{"role": "user", "content": "我刚才问你什么了？"}]
    },
    config={"configurable": {"thread_id": "abc123"}},   # ← 相同thread_id
):
    print(chunk, end="\n\n")
# Agent会回答："你刚才问了北京今天的天气"

# ===== 第3次调用（不同thread_id → 无记忆） =====
print("=== 第3次调用（新会话） ===")
for chunk in agent.stream(
    input={
        "messages": [{"role": "user", "content": "我刚才问你什么了？"}]
    },
    config={"configurable": {"thread_id": "xyz789"}},   # ← 不同thread_id
):
    print(chunk, end="\n\n")
# Agent会回答："这是我们第一次对话，你还没有问过任何问题"