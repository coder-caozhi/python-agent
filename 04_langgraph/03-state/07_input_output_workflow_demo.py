"""
目标：通过问题搜索答案
1. 定义图状态： state
2. 定义节点函数： node
3. 通过状态创建图实例： graph
4. 添加节点： 将节点注册到图中
5. 添加边： 顺序边 条件边
6. 编译图
7. 启动工作流: 按照节点和边的注册流程自动执行
8. 输出结果

问题：大模型中的“幻觉”是什么意思？
"""
import time
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1.1 定义图状态：全局状态
class MyState(TypedDict):
    query: str  # 用户输入的问题
    rag_result: str  # 权威RAG搜索结果
    web_search_result: str  # 实时网搜结果
    final_answer: str  # 大模型的最终回复

# 1.2 定义输入状态
# 只允许输入状态包含query信息
class InputSchema(TypedDict):
    query: str  # 用户输入的问题

# 1.3 定义输出状态
# 只允许输出状态包含final_answer信息
class OutputSchema(TypedDict):
    final_answer: str  # 最终回复

# 1.4 节点状态（node_state）
class SearchState(TypedDict):
    rag_result: str  # 权威RAG搜索结果
    web_search_result: str  # 实时网络搜索结果


# 2. 定义节点函数
# 2.1 权威RAG搜索
def rag_search_node(state: MyState):
    # 1. 获取用户输入的问题
    print("rag_search_node【权威知识库检索】正在搜索权威RAG结果...")
    query = state.get("query")

    # 2. 模拟向量搜索的时间延迟
    time.sleep(2)
    rag_result = f"rag_search_node【权威知识库检索结果】{query}：指大语言模型（LLM）生成的内容虽然看似合理且流畅，但实际上与源上下文或现实世界事实不符，甚至完全虚构的现象。"

    # 3. 将搜索结果写入到state图状态中
    # 每个节点都需要返回状态信息
    # 最好返回状态的增量信息

    # 全量信息的返回
    # state["rag_result"] = rag_result
    # return state

    # 增量信息的返回，可以是dict类型
    print("rag_search_node【权威知识库检索结果】检索完成：")
    return {
        "rag_result": rag_result
    }


# 2.2 网络搜索
def web_search_node(state: MyState):
    # 1. 获取用户输入的问题
    print("web_search_node【实时网络检索】正在搜索最新网络内容...")
    query = state.get("query")

    # 2. 模拟网络搜索的时间延迟
    time.sleep(2)
    web_search_result = f"web_search_node【实时网络检索结果】{query}：常被戏称为AI在“一本正经地胡说八道”。比如AI可能会捏造不存在的历史事件、错误的代码库引用或虚假的论文出处。"

    # 3. 将搜索结果写入到state图状态中
    print("web_search_node【实时网络检索结果】检索完成：")
    return {
        "web_search_result": web_search_result
    }


# 2.3 定义最终回复节点
def final_answer_node(state: SearchState):
    # 1. 从图状态中获取多路搜索的结果
    print("final_answer_node【将多路搜索结果进行融合】...")
    rag_result = state.get("rag_result")
    web_search_result = state.get("web_search_result")

    # 2. 模拟调用大模型
    time.sleep(2)
    final_answer = f"""
final_answer_node🤖【AI助手总结】：
答案:
{rag_result}
{web_search_result}
需要我教你如何降低模型的幻觉率吗❓
"""

    # 3. 将搜索结果写入到state图状态中
    print("final_answer_node【AI助手的最终回答】回答生成结束")
    return {
        "final_answer": final_answer
    }


# 3. 通过状态创建图实例
graph = StateGraph(
    state_schema=MyState, # 全局状态
    input_schema=InputSchema, #输入状态
    output_schema=OutputSchema # 输出状态
)

# 4. 添加节点
# 方式1：用函数名做节点名
graph.add_node(rag_search_node)
graph.add_node(web_search_node)
graph.add_node(final_answer_node)

# 方式2：为节点起一个别名
# graph.add_node("rag_search_node", rag_search_node)
# graph.add_node("web_search_node", web_search_node)
# graph.add_node("final_answer_node", final_answer_node)

# 5. 添加边
graph.add_edge(START, "rag_search_node")
graph.add_edge(START, "web_search_node")
graph.add_edge("rag_search_node", "final_answer_node")
graph.add_edge("web_search_node", "final_answer_node")
graph.add_edge("final_answer_node", END)

# 6. 编译图
compiled_graph = graph.compile()

# 7. 启动工作流
state = compiled_graph.invoke({
    "query": "大模型中的“幻觉”是什么意思？",
    "rag_result": "abc"
})

# 8. 输出结果
print(state["final_answer"])

# 9. 打印工作流的图结构
compiled_graph.get_graph().print_ascii()

#总结:
# 通过线程池的方式启动多个线程执行并发的搜索流程