import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model

# 加载环境变量
load_dotenv(find_dotenv())

# 2.初始化模型
model = init_chat_model(
    model=os.getenv("LLM_MODEL", "deepseek-chat"),
    model_provider="openai"
)


# todo: 定义个langgraph图   start => 图节点 => end
# 1. 定义 State (必须包含 messages)
class SubState(TypedDict):
    # 必须这么写
    messages: Annotated[list, add_messages]

# 2. 定义各节点函数
def sub_agent_node(state:SubState):
    # 1.获取参数
    # messages -> 看我们这个langgraph在deepagent规划的对应的位置!
    # deep_agent ( 1.x 2.j 3.langgaph) -> 2 -> 3 [messages:[2,3]] -> 1 -> 输出结果
    messages = state["messages"]
    print(f"[langgraph]的节点,输入的参数:{messages}")
    # 2.编写业务
    print(f"---------执行业务------------")
    # 3.返回结果
    return {
        "messages":[
            AIMessage(content="langgraph子智能体的返回结果")
        ]
    }

# 3. 定义图对象
graph_builder = StateGraph(state_schema=SubState)
# 添加节点
graph_builder.add_node(sub_agent_node) # 添加节点(函数) 函数 -> 节点就是函数名
#graph_builder.add_node("graph_builder",graph_builder) # ("节点名",函数名)

# 添加边 ""
graph_builder.set_entry_point("sub_agent_node")
graph_builder.add_edge("sub_agent_node",END)

graph = graph_builder.compile()

# graph -> deep_agent
langgraph_sub_agent = CompiledSubAgent(
    name = "langgraph_sub_agent",
    description="负责用户信息查询的子智能体!",
    runnable=graph
)

deep_agent = create_deep_agent(
    model=model,
    system_prompt="""
      综合智能体,不负责具体的业务! 具体的工作调用langgraph_sub_agent子智能体执行!!
    """,
    subagents=[langgraph_sub_agent]
)

result = deep_agent.invoke(input={
    "messages":[
        HumanMessage(content="请帮我查询root用户信息!")
    ]
})

print(result["messages"][-1].content)