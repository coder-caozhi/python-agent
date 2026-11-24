import operator
from typing import List, TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, add_messages


# 自定义Reducer:为每一条新消息添加一个图标前缀,并且是增量列表的形式
def custom_add_messages(
    existing_messages: List[BaseMessage],
    new_messages: List[BaseMessage]
) -> List[BaseMessage]:

    print("Adding messages:")

    # 1. 健壮性判断，如果existing_messages为None，则初始化为空列表
    if existing_messages is None:
        existing_messages = []

    # 2. 创建图标映射字典
    # key的定义: 约定大于编程
    icon_map = {
        'system': '🔧 [系统]',
        'human': '👤 [用户]',
        'ai': '🤖 [AI]'
    }

    # 2. 定义一个处理后的消息列表
    processed_messages = []
    for msg in new_messages:
        icon = icon_map.get(msg.type, '')
        if isinstance(msg, HumanMessage):
            processed_messages.append(HumanMessage(content=f"{icon}  {msg.content}"))
        elif isinstance(msg, SystemMessage):
            processed_messages.append(SystemMessage(content=f"{icon}  {msg.content}"))
        elif isinstance(msg, AIMessage):
            processed_messages.append(AIMessage(content=f"{icon}  {msg.content}"))
        else:
            processed_messages.append(msg)

    return existing_messages + processed_messages


# 自定义搜索结果 Reducer：为结果添加序号
def custom_add_search_results(
        existing_results: List[str],
        new_results: List[str]
) -> List[str]:

    """
    自定义搜索结果追加函数，为每个结果添加序号
    """
    if existing_results is None:
        existing_results = []

    # 计算新序号的起始值
    start_index = len(existing_results) + 1

    # 处理每个结果
    processed_results = []
    for i, result in enumerate(new_results, start=start_index):
        processed_results.append(f"📌 步骤{i}: {result}")

    # 返回更新后的结果列表
    return existing_results + processed_results



# 1. 定义图状态 - 所有字段均未指定reducer，故默认为覆盖
# 结论:默认情况下,在每个阶段中为state赋的值,都是覆盖行为
class AgentState(TypedDict):
    query: str

    # 自定义Reducer函数的设置
    messages: Annotated[List[BaseMessage], custom_add_messages]  # 历史消息列表

    ## 自定义Reducer函数的设置
    search_results: Annotated[List[str], custom_add_search_results]    # 搜索结果列表


# 2. 节点函数：输入处理
def input_node(state: AgentState):
    query = state["query"]
    new_message = HumanMessage(content=f"用户问题: {query}")

    # 持久化到mongodb数据库中 TODO

    # 返回新列表，将完全替换掉state["messages"]的旧列表
    return {"messages": [new_message]}

# 3. 节点函数：搜索处理
def search_node(state: AgentState):
    query = state["query"]


    # 调用了大模型 ChatOpenAI invoke response TODO

    query_result = f"模拟搜索结果：关于'{query}'的相关信息..."
    search_msg = AIMessage(content=f"搜索完成: {query_result}")

    # 返回新列表，将完全替换掉state["search_msg"]和state["query_result"]的旧列表
    return {
        "messages": [search_msg],
        "search_results": [query_result]
    }


# 4. 节点函数：生成最终回复
def response_node(state: AgentState):

    context = state["search_results"] # 此时search_results只包含上一个节点的单条结果
    query = state["query"]

    # 模拟调用大模型  llm invoke response.content TODO

    final_response = f"基于搜索结果，对问题'{query}'的回答是：{context} "
    ai_response = AIMessage(content=final_response)

    return {
        "messages": [ai_response], # 再次覆盖整个messages列表
        "search_results": [f"最终回复已生成"] # 覆盖整个search_results列表
    }


def build_graph():

    # 1. 创建工作流实例
    workflow = StateGraph(AgentState)

    # 2. 添加节点
    workflow.add_node("input", input_node)
    workflow.add_node("search", search_node)
    workflow.add_node("response", response_node)

    # 设置边
    workflow.add_edge("input", "search")
    workflow.add_edge("search", "response")

    # 设置入口和出口
    workflow.set_entry_point("input")
    workflow.set_finish_point("response")

    return workflow.compile()

if __name__ == '__main__':

    # 初始化图实例
    app = build_graph()

    # 从mongodb中获取历史聊天记录 TODO
    # 初始化当前的系统提示词

    # 设置初始状态
    initial_state = {
        "query": "Python编程最佳实践",
        "messages": [
            HumanMessage(content="你好。"),
            AIMessage(content="你好,请问有什么需要帮助的吗?"),
            SystemMessage(content="你是一个AI助手，正在进行信息检索任务。")
        ],
        # "search_results": []
    }

    # 执行流程
    result = app.invoke(initial_state)

    print("最终状态")
    print(f"query: {result['query']}")

    print("消息历史")
    for i, msg in enumerate(result["messages"]):
        print(f"Message {i+1} {msg.type}: {msg.content}")

    print("搜索结果")
    for i, res in enumerate(result["search_results"]):
        print(f"Message {i + 1} {res}")

