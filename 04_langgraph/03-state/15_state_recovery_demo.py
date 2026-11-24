# 1. 构建图状态
import os
import sqlite3
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. 定义状态
class MyState(TypedDict):
    key_1: str
    key_2: str
    key_3: str


# 2. 定义节点函数
def node_1(state: MyState) -> MyState:
    print('node_1状态为', state)
    return {"key_1": "value_1"}


def node_2(state: MyState) -> MyState:
    print('node_2状态为', state)
    # raise Exception("模拟node_2节点报错")
    return {"key_2": "value_2"}


def node_3(state: MyState) -> MyState:
    print('node_3状态为', state)
    return {"key_3": "value_3"}

# 3. 构建图
def build_graph():
    workflow = StateGraph(MyState)
    workflow.add_node(node_1)
    workflow.add_node(node_2)
    workflow.add_node(node_3)
    workflow.add_edge(START, "node_1")
    workflow.add_edge("node_1", "node_2")
    workflow.add_edge("node_1", "node_3")
    workflow.add_edge("node_2", END)
    workflow.add_edge("node_3", END)
    return workflow


# 4. 主函数
def demo_langgraph():
    # 1. 构建Connection对象
    # database：指定数据库保存的位置
    # check_same_thread=False 默认True
    # SQLite很"谨慎"，只允许创建它的那个线程使用它
    # 改成 False：允许其他线程也使用这个数据库连接
    # 因为LangGraph可能会在后台用不同的线程操作数据库，如果不改会报错
    os.makedirs("./sqlite_data", exist_ok=True)
    conn = sqlite3.connect(database="./sqlite_data/langgraph_sqlite.db", check_same_thread=False)
    # 2. 通过connection对象构建checkpointer实例
    # uv add langgraph-checkpoint-sqlite
    checkpointer = SqliteSaver(conn)

    # 3. 构建图
    graph = build_graph()

    # 4. 编译图时传入 Checkpointer
    app = graph.compile(checkpointer=checkpointer)

    # 5. 定义config
    config = {"configurable": {"thread_id": "a1"}}

    # 6. 调用时传入config
    # result = app.invoke({}, config=config)

    # 6. 从状态中恢复：传入None
    result = app.invoke(None, config=config)

    # 7. 打印结果
    print(result)
    # app.get_graph().print_ascii()


if __name__ == "__main__":
    demo_langgraph()