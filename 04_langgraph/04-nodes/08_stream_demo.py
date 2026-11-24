import operator
import time
from typing import Annotated, List, TypedDict
from unittest import main

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

from llm_config import llm_config

# 初始化 LLM
llm_client = init_chat_model(
    model=llm_config.llm_model,
    model_provider=llm_config.model_provider,
    base_url=llm_config.base_url,
    api_key=llm_config.api_key,
)

# 1. 定义图状态
class State(TypedDict):
    input: str
    messages: Annotated[List[BaseMessage], operator.add]
    current_step: str


# 2. 定义节点：接收用户输入
def node_input(state: State):
    """接收用户输入"""
    input = state["input"]
    return {
        "messages": [HumanMessage(content=input)],
        "current_step": "接收用户输入"
    }

# 3. 定义节点：执行RAG检索流程
def node_processing(state: State, runtime: Runtime):
    """
    模拟中间处理过程，并使用 writer 输出自定义流式数据
    这对应 stream_mode="custom"
    """
    steps = ["正在分析意图...", "正在检索知识库...", "正在构建Prompt..."]

    # 获取stream_writer
    writer = runtime.stream_writer

    for i, step in enumerate(steps):
        # 模拟中间处理过程
        time.sleep(1)
        # print(f"[Step {i+1}/{len(steps)}] {step}")

        # 会输出到图外侧的生成器结果中
        writer({
            "step_index": i + 1,
            "description": step,
            "timestamp": time.time()
        })


    return {"current_step": "RAG检索处理完成"}

# 4. 定义节点：生成答案
def node_generation(state: State):
    """
    LLM 生成答案
    LangGraph 的 stream_mode="messages" 会自动捕获 LLM 的流式输出
    """
    # 调用 LLM（AIMessage）
    response = llm_client.invoke(state["messages"])

    return {
        "messages": [response],
        "current_step": "生成完成"
    }


# 5. 构建图
def build_graph():
    graph = StateGraph(State)
    graph.add_node("input", node_input)
    graph.add_node("process", node_processing)
    graph.add_node("generate", node_generation)

    graph.add_edge(START, "input")
    graph.add_edge("input", "process")
    graph.add_edge("process", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


# 4. 演示不同的流式输出模式
def demo_langgraph():

    initial_state = {"input": "我是谁", "messages": [], "current_step": "start"}
    app = build_graph()

    # 0. 非流式数出测试: 只能在所有节点执行完毕之后输出整个工作流的最终状态
    result = app.invoke(input=initial_state)
    print("执行结束")
    print(result)



    # 1. 流式输出(generator)  values ： 输出的是状态的完整值
    # for state in app.stream(initial_state, stream_mode="values"):
    #     print(f" step = {state.get('current_step')}, state = {state}")

    # 2. 流式输出: updates  状态值增量更新
    # for state in app.stream(initial_state, stream_mode="updates"):
    #     print(f" step = {state.get('current_step')}, state = {state}")

    # 3. 流式输出： custom 自定义节点输出的流
    # for state in app.stream(initial_state, stream_mode="custom"):
    #     print(f" step = {state.get('current_step')}, state = {state}")

    # 4. 流式输出： messages 只输出大模型的messages中的信息
    # last_node = None
    # for chunk, metadata in app.stream(initial_state, stream_mode="messages"):
    #     # print(chunk, metadata)
    #     node_name = metadata.get("langgraph_node")
    #     # print(f"[Node {node_name}] {chunk.content}")
    #     if node_name != last_node:
    #         last_node = node_name
    #         print(f"\n[{node_name}]", end="")
    #     print(chunk.content, end="")
    # print()
    #
    # 5. Mode: debug (调试模式)
    # for event in app.stream(initial_state, stream_mode="debug"):
    #     print(f"Debug Event: {event['type']} - {event.get('payload', {}).get('name')}")
    # print("... (省略后续 debug 信息)")

    # 6. Mixed Mode (混合模式)
    # for mode, data in app.stream(initial_state, stream_mode=["updates", "custom"]):
    #     if mode == "updates":
    #         print(f" step = {state.get('current_step')}, state = {state}")
    #     elif mode == "custom":
    #         print(f" step = {state.get('current_step')}, state = {state}")
    #

if __name__ == '__main__':
    demo_langgraph()

